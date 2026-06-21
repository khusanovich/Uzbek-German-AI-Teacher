"""Lesson endpoints: list units, run a lesson turn, get audio for a reply."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.prompts.tutor_prompt import CEFR, LessonContext, build_system_prompt
from app.curriculum.units import get_units, get_unit
from app.services.llm import tutor_reply
from app.services.tts import split_by_language

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
def list_units(level: CEFR):
    return [u.__dict__ for u in get_units(level)]


@router.post("/turn", response_model=TurnResponse)
def run_turn(req: TurnRequest):
    unit = get_unit(req.unit_id)
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
