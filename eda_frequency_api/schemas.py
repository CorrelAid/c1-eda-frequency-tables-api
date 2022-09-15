from pydantic import BaseModel
from pydantic.schema import Optional
from datetime import datetime
from typing import List, Union

class OverallStats(BaseModel):
    overall_n: int
    
class Frequencies(BaseModel):
    sub_question_id: Union[str, None] 
    value: Union[int, None] 
    value_label: Union[str, None] 
    count: int

class NestedValueCounts(BaseModel):
    value: int
    count: int
    
class NestedFrequencies(BaseModel):
    sub_question_id: str
    value_counts: List[NestedValueCounts]
    
class QuestionStats(BaseModel):
    question_item_id: str
    n: int
    type: str
    frequencies: Union[List[NestedFrequencies], List[Frequencies]]
    
    
# class SingleChoice(BaseModel):
#     question_item_id: str
#     value_counts: dict

# class MultipleChoice(BaseModel):
#     question_item_id: str
#     value_counts: dict

    