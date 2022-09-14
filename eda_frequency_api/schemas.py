from pydantic import BaseModel
from pydantic.schema import Optional
from datetime import datetime
from typing import List

class OverallStats(BaseModel):
    overall_n: int
    
class ValueCounts(BaseModel):
    value: int
    value_label: str
    count: int
    
class QuestionStats(BaseModel):
    question_item_id: str
    n: int
    value_counts: List[ValueCounts]
    
# class SingleChoice(BaseModel):
#     question_item_id: str
#     value_counts: dict

# class MultipleChoice(BaseModel):
#     question_item_id: str
#     value_counts: dict

    