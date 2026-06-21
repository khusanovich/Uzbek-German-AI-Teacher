"""
Fixed curriculum skeleton. The LLM teaches WITHIN a unit; it never invents
the syllabus. Store this in Postgres in production; kept here as plain data
so the structure is obvious and easy to seed.
"""

from dataclasses import dataclass, field
from app.prompts.tutor_prompt import CEFR


@dataclass
class Unit:
    id: str
    level: CEFR
    title: str
    objectives: list[str]
    target_vocab: list[str] = field(default_factory=list)


A1_1_UNITS: list[Unit] = [
    Unit(
        id="a1_1_u1",
        level=CEFR.A1_1,
        title="Begruessung und Vorstellung",
        objectives=[
            "Sich begruessen und verabschieden",
            "Den eigenen Namen nennen und nach dem Namen fragen",
            "Das Verb 'heissen' im Singular",
        ],
        target_vocab=["hallo", "tschuess", "ich heisse", "wie heisst du", "guten Tag"],
    ),
    Unit(
        id="a1_1_u2",
        level=CEFR.A1_1,
        title="Woher kommst du?",
        objectives=[
            "Ueber Herkunft sprechen (kommen aus)",
            "Laendernamen verwenden",
            "Das Verb 'kommen' im Singular",
        ],
        target_vocab=["ich komme aus", "woher", "Usbekistan", "Deutschland", "das Land"],
    ),
    Unit(
        id="a1_1_u3",
        level=CEFR.A1_1,
        title="Zahlen 0-20",
        objectives=[
            "Zahlen von 0 bis 20 erkennen und sprechen",
            "Nach Telefonnummer / Alter fragen",
        ],
        target_vocab=["null", "eins", "zwei", "zehn", "zwanzig", "wie alt"],
    ),
    Unit(
        id="a1_1_u4",
        level=CEFR.A1_1,
        title="Artikel: der, die, das",
        objectives=[
            "Bestimmte Artikel einfuehren",
            "Grammatisches Geschlecht als Konzept verstehen",
            "Substantive immer mit Artikel lernen",
        ],
        target_vocab=["der Mann", "die Frau", "das Kind", "der Tisch", "die Lampe"],
    ),
    Unit(
        id="a1_1_u5",
        level=CEFR.A1_1,
        title="Praesens regelmaessiger Verben",
        objectives=[
            "Konjugation regelmaessiger Verben im Singular und Plural",
            "Personalpronomen ich/du/er/sie/es/wir/ihr/sie",
        ],
        target_vocab=["machen", "lernen", "wohnen", "spielen", "arbeiten"],
    ),
]


def get_units(level: CEFR) -> list[Unit]:
    if level == CEFR.A1_1:
        return A1_1_UNITS
    return []  # add A1.2, A2.1, ... as you build them


def get_unit(unit_id: str) -> Unit | None:
    for unit in A1_1_UNITS:
        if unit.id == unit_id:
            return unit
    return None
