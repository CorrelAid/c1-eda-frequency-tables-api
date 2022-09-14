from sqlalchemy.orm import Session
# from eda_frequency_api.models import *
import json
from eda_frequency_api.helpers import sql_query, sql_to_single, sql_to_lst, M_loop_transform
# from eda_frequency_api.cache import r


# https://docs.sqlalchemy.org/en/14/tutorial/data.html#tutorial-working-with-data


#### Helper functions


def query_overall_stats(db):
    query = f'''
    SELECT COUNT(respondent_id) FROM respondent_v1
    '''
    x = query_single_result(db, query, "count")

    return {"overall_n": x}


def query_question_stats(db, question_id):

    # this query only works with single choice questions, because also unchecked multiple choice anwers count as response.
    query_string_n_question_single = f'''
    SELECT question_item_id, COUNT(*) FROM q_response_labelled_de_v1 WHERE question_item_ID = '{question_id}' GROUP BY question_item_id
    '''
    
    query_string_value_counts_Y = f'''
    SELECT value, value_label, COUNT(value) FROM q_response_labelled_de_v1 WHERE question_item_id = '{question_id}' GROUP BY value, value_label
    '''
    
    typ = sql_to_single(db, f"SELECT type_major FROM question_item_v1 WHERE question_item_id = '{question_id}'", "type_major")
    
    if typ == "Single Choice":
        return {"question_item_id": question_id, "n": sql_to_single(db, query_string_n_question, "count"), "type": typ, "value_counts": sql_to_lst(db, query_string_value_counts_Y)}
    elif typ == "Multiple Choice":
        value_counts = M_loop_transform(db, question_id)
        # alternative way to get n of question
        n = sum(value_counts.values())
        return {"question_item_id": question_id, "n": n, "type": typ, "value_counts": value_counts}


# def query_single_choice(db, question_id):
#     query = f'''
#     SELECT value, COUNT(value) FROM q_response_labelled_de_v1 WHERE question_item_id = '{question_id}' GROUP BY value 
#     '''

#     x = sql_to_lst(db, query)

#     return {"question_item_id": question_id, "value_counts": x}


# def query_multiple_choice(db, question_id):
#     query = f'''
#     SELECT subquestion_id, value, COUNT(value) FROM q_response_labelled_en_v1 WHERE  question_item_id IN ( SELECT question_item_id from q_response_labelled_en_v1 where question_item_id = '{question_id}') GROUP BY value, subquestion_id
#     '''

#     x = sql_to_lst_mult(db, query)

#     return {"question_item_id": question_id, "value_counts": x}


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
