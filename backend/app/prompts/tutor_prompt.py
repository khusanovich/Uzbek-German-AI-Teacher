"""
Tutor system prompt builder.

The whole Uzbek -> German instruction-language switch lives here.
It is a function of (a) the learner's CEFR level and (b) an optional
per-user override, NOT a hardcoded cutoff. Inject the result as the
system prompt for each lesson turn.
"""

from enum import Enum
from dataclasses import dataclass


class CEFR(str, Enum):
    A1_1 = "A1.1"
    A1_2 = "A1.2"
    A2_1 = "A2.1"
    A2_2 = "A2.2"
    B1_1 = "B1.1"
    B1_2 = "B1.2"
    B2 = "B2"
    C1 = "C1"


# Ordered for comparisons ("is the learner at or above X?")
_LEVEL_ORDER = [
    CEFR.A1_1, CEFR.A1_2, CEFR.A2_1, CEFR.A2_2,
    CEFR.B1_1, CEFR.B1_2, CEFR.B2, CEFR.C1,
]


def level_at_or_above(level: CEFR, threshold: CEFR) -> bool:
    return _LEVEL_ORDER.index(level) >= _LEVEL_ORDER.index(threshold)


class InstructionLanguage(str, Enum):
    UZBEK = "uzbek"
    GERMAN_SCAFFOLDED = "german_scaffolded"  # German + Uzbek glosses for new terms
    GERMAN = "german"


def default_instruction_language(level: CEFR) -> InstructionLanguage:
    """Default policy. A per-user setting can override this."""
    if level_at_or_above(level, CEFR.B1_1):
        return InstructionLanguage.GERMAN
    if level_at_or_above(level, CEFR.A2_2):
        return InstructionLanguage.GERMAN_SCAFFOLDED
    return InstructionLanguage.UZBEK


@dataclass
class LessonContext:
    level: CEFR
    unit_title: str
    objectives: list[str]          # grammar/vocab goals for THIS unit
    target_vocab: list[str]        # German words/phrases to introduce
    instruction_language: InstructionLanguage | None = None  # override


_LANG_BLOCK = {
    InstructionLanguage.UZBEK: (
        "Tushuntirishlaringizni TO'LIQ o'zbek tilida bering. Grammatik qoidalar, "
        "izohlar va ko'rsatmalar o'zbek tilida bo'lsin. Faqat nemis tilidagi "
        "MISOLLAR (so'zlar, jumlalar) nemis tilida qoladi va ularga o'zbekcha "
        "tarjima beriladi. Hech qachon o'zbek tilini nemis tili bilan aralashtirmang."
    ),
    InstructionLanguage.GERMAN_SCAFFOLDED: (
        "Erklaere auf einfachem Deutsch (A2-Niveau). Verwende kurze Saetze. "
        "Wenn ein neuer Grammatik-Fachbegriff vorkommt, gib EINMAL die usbekische "
        "Uebersetzung in Klammern dahinter. Der Rest bleibt auf Deutsch."
    ),
    InstructionLanguage.GERMAN: (
        "Unterrichte vollstaendig auf Deutsch. Keine usbekischen Uebersetzungen, "
        "ausser der Lernende fragt ausdruecklich danach."
    ),
}


SYSTEM_TEMPLATE = """\
Du bist ein geduldiger, praeziser Deutschlehrer fuer usbekische Muttersprachler.

# Instruction language
{lang_block}

# Current learner level
CEFR: {level}

# This unit
Title: {unit_title}
Learning objectives:
{objectives}
Target vocabulary to introduce (German): {vocab}

# Teaching rules
- Stay strictly within this unit's objectives. Do NOT introduce grammar or
  vocabulary from later units, even if the learner asks something advanced;
  briefly note it's "spaeter" and steer back.
- Every German example sentence must be natural and grammatically correct.
- When you give a German example, mark it clearly so the audio layer can
  send it to German TTS. Wrap every German example exactly like:
  [[de]]Ich heisse Anna.[[/de]]
  Put any explanation/translation OUTSIDE those tags.
- Be concise. One concept at a time. End each turn with one small check
  question so the learner produces German.
- If the learner makes a mistake, correct gently: show the wrong form, the
  right form, and a one-line reason.
"""


def build_system_prompt(ctx: LessonContext) -> str:
    lang = ctx.instruction_language or default_instruction_language(ctx.level)
    objectives = "\n".join(f"- {o}" for o in ctx.objectives)
    return SYSTEM_TEMPLATE.format(
        lang_block=_LANG_BLOCK[lang],
        level=ctx.level.value,
        unit_title=ctx.unit_title,
        objectives=objectives,
        vocab=", ".join(ctx.target_vocab),
    )
