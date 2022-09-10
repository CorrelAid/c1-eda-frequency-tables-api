from sqlalchemy.orm import Session
from eda_frequency_api.models import *
from sqlalchemy import select, text
import json
from eda_frequency_api.cache import r


# https://docs.sqlalchemy.org/en/14/tutorial/data.html#tutorial-working-with-data

def sql_query(db, query):
    return db.execute(text(query))


def sql_to_dict(db, query):
    dct = {}
    result = sql_query(db, query).all()
    print(result)
    keys = list(dict(result[0]).keys())
    print(keys)
    for row in result:
        print(row)
        dct[row[keys[0]]] = row[keys[1]]
    return dct


def sql_to_dict_mult(db, query):
    dct = {}
    result = sql_query(db, query).all()
    print(result)
    keys = list(dict(result[0]).keys())
    print(keys)
    for row in result:
        print(row)
        dct[row[keys[0]]] = [row[keys[1]], row[keys[2]]]
    return dct


def query_single_result(db, query):
    result = sql_query(db, query).all()
    x = []
    for row in result:
        x.append(row["count"])
    return x[0]


def query_overall_freqs(db):
    query = f'''
    SELECT COUNT(respondent_id) FROM respondent_v1
    '''
    x = query_single_result(db, query)

    return {"overall_n": x}


def query_n_question(db, question_id):

    query = f'''
    SELECT question_item_id, COUNT(*) FROM q_response_labelled_de_v1 WHERE question_item_ID = '{question_id}' GROUP BY question_item_id
    '''

    x = query_single_result(db, query)

    return {"question_item_id": question_id, "n": x}


def query_single_choice(db, question_id):
    query = f'''
    SELECT value, COUNT(value) FROM q_response_labelled_de_v1 WHERE question_item_id = '{question_id}' GROUP BY value 
    '''

    x = sql_to_dict(db, query)

    return {"question_item_id": question_id, "value_counts": x}


def query_multiple_choice(db, question_id):
    query = f'''
    SELECT subquestion_id, value, COUNT(value) FROM q_response_labelled_en_v1 WHERE  question_item_id IN ( SELECT question_item_id from q_response_labelled_en_v1 where question_item_id = '{question_id}') GROUP BY value, subquestion_id
    '''

    x = sql_to_dict_mult(db, query)

    return {"question_item_id": question_id, "value_counts": x}


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
