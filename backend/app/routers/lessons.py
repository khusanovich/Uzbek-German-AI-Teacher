"""Lesson endpoints: list units, run a lesson turn, get audio for a reply."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.prompts.tutor_prompt import CEFR, LessonContext, build_system_prompt
from app.services.llm import tutor_reply
from app.services.tts import split_by_language
from app.database import get_db
from app.models import Unit as UnitModel

router = APIRouter(prefix="/lessons", tags=["lessons"])


class TurnRequest(BaseModel):
    unit_id: str
    learner_level: CEFR
    message: str
    history: list[dict] = []


class TurnResponse(BaseModel):
    reply: str
    audio_chunks: list[dict]  # [{"lang": "de"|"uz", "text": ...}]


@router.get("/units/{level}")
def list_units(level: CEFR, db: Session = Depends(get_db)):
    """Get all units for a given CEFR level from the database."""
    units = db.query(UnitModel).filter(UnitModel.level == level.value).all()
    return [
        {
            "id": u.id,
            "level": u.level,
            "title": u.title,
            "objectives": u.objectives,
            "target_vocab": u.target_vocab,
        }
        for u in units
    ]


@router.post("/turn", response_model=TurnResponse)
def run_turn(req: TurnRequest, db: Session = Depends(get_db)):
    """Run a lesson turn with the tutor for a specific unit."""
    unit = db.query(UnitModel).filter(UnitModel.id == req.unit_id).first()
    if unit is None:
        raise HTTPException(404, "unknown unit")

    ctx = LessonContext(
        level=req.learner_level,
        unit_title=unit.title,
        objectives=unit.objectives,
        target_vocab=unit.target_vocab,
    )
    system = build_system_prompt(ctx)
    reply = tutor_reply(system, req.history, req.message)
    chunks = [{"lang": l, "text": t} for l, t in split_by_language(reply)]
    return TurnResponse(reply=reply, audio_chunks=chunks)
