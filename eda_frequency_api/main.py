import uvicorn
import os
import sys
import databases
import sqlalchemy
from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

import eda_frequency_api.models 
from eda_frequency_api.schemas import OverallStats, QuestionStats
from eda_frequency_api.queries import *
from eda_frequency_api.database import SessionLocal,engine,metadata
from eda_frequency_api.helpers import generate_model


app = FastAPI(title="EDA freq api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@app.get("/",response_model=OverallStats)
def root(db: Session = Depends(get_db)):
    x = query_overall_stats(db)
    return x

@app.get("/question_stats/{question_id}",response_model=QuestionStats, response_model_exclude_none=True)
def root(question_id, db: Session = Depends(get_db)):
    return query_question_stats(db, question_id)

# @app.get("/multiple_choice/{question_id}",response_model=MultipleChoice)
# def root(question_id, db: Session = Depends(get_db)):
#     x = query_multiple_choice(db, question_id)
#     return x

def start():
    """Launched with `poetry run start` at root level"""
    # Generating sqlalchemy model 
    generate_model(engine=engine, metadata=metadata, outfile='eda_frequency_api/models.py')
    uvicorn.run("eda_frequency_api.main:app", host="0.0.0.0", port=8000, reload=True)