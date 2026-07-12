"""
Pydantic schemas used to constrain Ollama's structured JSON output via the
`format` parameter. These are separate from FastAPI's request/response
models in main.py — these exist purely to force the LLM's output into an
exact, predictable shape at the token-generation level, so there's no more
need to guess or unwrap different shape variants after the fact.
"""
from pydantic import BaseModel
from typing import Literal


class ValidationResult(BaseModel):
    verdict: Literal["supported", "contradicted", "not_found"]
    confidence: Literal["high", "low"]
    explanation: str
    suggestion: str


class ClaimsList(BaseModel):
    claims: list[str]


class Contradiction(BaseModel):
    claim_a: str
    claim_b: str
    explanation: str


class ContradictionsList(BaseModel):
    contradictions: list[Contradiction]


class QuizQuestion(BaseModel):
    question: str
    type: Literal["mcq", "truefalse", "open"]
    options: list[str]
    correct: str
    explanation: str


class QuizQuestionsList(BaseModel):
    questions: list[QuizQuestion]


class GradeResult(BaseModel):
    correct: bool
    feedback: str
