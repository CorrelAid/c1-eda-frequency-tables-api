from pydantic import BaseModel
from pydantic.schema import Optional
from datetime import datetime

class OverallFreqs(BaseModel):
    overall_n: int
    
class NQuestion(BaseModel):
    question_item_id: str
    n: int

class SingleChoice(BaseModel):
    question_item_id: str
    value_counts: dict

class MultipleChoice(BaseModel):
    question_item_id: str
    value_counts: dict

    