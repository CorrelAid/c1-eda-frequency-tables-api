from sqlalchemy.orm import Session
# from eda_frequency_api.models import *
import json
from eda_frequency_api.helpers import sql_query, sql_to_single, single_choice_transform, multiple_choice_transform, numeric_transform
# from eda_frequency_api.cache import r


# https://docs.sqlalchemy.org/en/14/tutorial/data.html#tutorial-working-with-data


#### Helper functions


def query_overall_stats(db):
    query = f'''
    SELECT COUNT(respondent_id) FROM respondent_v1
    '''
    x = sql_to_single(db, query, "count")

    return {"overall_n": x}


def query_question_stats(db, question_id):

    # determining n of question
    query_string_n_question = f'''
    SELECT count(DISTINCT respondent_id) FROM q_response_v1 WHERE question_item_id = '{question_id}' AND value IS NOT NULL
    '''
    
    # detecting type of question
    typ = sql_to_single(db, f"SELECT type_major FROM question_item_v1 WHERE question_item_id = '{question_id}'", "type_major")
    
     # value counts for single choice
    query_string_value_counts_single_choice= f'''
    SELECT value, value_label, COUNT(value) FROM q_response_labelled_de_v1 WHERE question_item_id = '{question_id}' GROUP BY value, value_label
    '''
    
    
    
    if typ == "Single Choice":
        return {"question_item_id": question_id, "n": sql_to_single(db, query_string_n_question, "count"), "type": typ, "value_counts": single_choice_transform(db, query_string_value_counts_single_choice)}
    elif typ == "Multiple Choice":
        return {"question_item_id": question_id, "n": sql_to_single(db, query_string_n_question, "count"), "type": typ, "value_counts": multiple_choice_transform(db, question_id)}
    elif typ == "Numeric":
        return {"question_item_id": question_id, "n": sql_to_single(db, query_string_n_question, "count"), "type": typ, "value_counts": numeric_transform(db, question_id)}


# def return_total_stats(db: Session):

#     cache_key = "total_stats"
#     cache_entry = r.get(cache_key)

#     if cache_entry:
#         print("using cache")
#         return json.loads(cache_entry)
#     else:
#         print("using db")
#         total_stats = query_total_stats(db)
#         r.set(cache_key,json.dumps(total_stats))
#         r.expire(cache_key, 1*3600)
#         return total_stats
