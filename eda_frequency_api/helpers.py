from sqlacodegen.codegen import CodeGenerator
from sqlalchemy import select, text
import io


def generate_model(engine, metadata, outfile=None):
    outfile = io.open(
        outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.render(outfile)


def sql_query(db, query):
    """ 
    Executes a SQL query inputted as string on the server
    """
    return db.execute(text(query))


def sql_to_lst(db, query):
    """ 
    Given a valid sql query result and existing columns, returns a dictionary.
    """
    lst = []
    result = sql_query(db, query).all()
    keys = list(dict(result[0]).keys())
    for row in result:
        dct = {}
        dct["value"] = int(row["value"])
        dct["value_label"] = row["value_label"]
        dct["count"] = row["count"]
        lst.append(dct)
    return lst


def sql_to_single(db, query, column):
    """ 
    Given a valid sql query result containing a single result(one row) and a existing column returns a single result as the type it was saved in db as.
    """
    result = sql_query(db, query).all()
    return result[0][column]


def M_loop_transform(db, question_id):
    
    sub_questions = sql_query(db, f"""
    SELECT subquestion_id FROM q_response_labelled_en_v1 WHERE question_item_id IN 
        (
        SELECT question_item_id from q_response_labelled_en_v1 where question_item_id = '{question_id}'
        ) 
    GROUP BY subquestion_id
    """)
    
    dct  = {}
    for i in sub_questions:
        query_string_value_counts_M = f'''
        SELECT value, value_label, COUNT(value) FROM q_response_labelled_de_v1 WHERE subquestion_id = '{i[0]}' GROUP BY value, value_label 
        '''
        x = sql_to_lst(db, query_string_value_counts_M)
        for y in x: 
            if y["value"] == 1:  
                dct[i[0]] = y["count"]
    print(dct)
    return dct