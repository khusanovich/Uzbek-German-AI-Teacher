from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import lessons, audio

app = FastAPI(title="Sprachassistent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lessons.router)
app.include_router(audio.router)


@app.get("/health")
def health():
    return {"status": "ok"}
