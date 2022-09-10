from pydantic import BaseModel
from pydantic.schema import Optional
from datetime import datetime

class OverallFreqs(BaseModel):
    overall_n: int
    
class NQuestion(BaseModel):
    question_item_id: str
    n: int
    
    
    

    