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


def sql_to_single(db, query, column):
    """ 
    Given a valid sql query result resulting in a single result(one row) and a existing column returns the data as the type it was saved in db as.
    """
    
    result = sql_query(db, query).all()
    
    return result[0][column]


def single_choice_transform(db, query, value_label: bool = True):
    """ 
    Given a valid sql query result returns a list.
    """
    
    lst = []
    
    result = sql_query(db, query).all()
    
    for row in result:
        dct = {}
        dct["value"] = int(row["value"])
        if value_label:
            dct["value_label"] = row["value_label"]
        dct["count"] = row["count"]
        lst.append(dct)
    
    return lst


def multiple_choice_transform(db, question_id):
    
    sub_questions = sql_query(db, f"""
    SELECT subquestion_id FROM q_response_labelled_en_v1 WHERE question_item_id IN 
        (
        SELECT question_item_id from q_response_labelled_en_v1 where question_item_id = '{question_id}'
        ) 
    GROUP BY subquestion_id
    """)
    
    lst = []
    dct  = {}
    
    for sub_question in sub_questions:
        query_string_value_counts_multiple_choice = f'''
        SELECT value, value_label, COUNT(value) FROM q_response_labelled_de_v1 WHERE subquestion_id = '{sub_question[0]}' GROUP BY value, value_label
        '''
        result = single_choice_transform(db, query_string_value_counts_multiple_choice)
        
        for row in result: 
            if row["value"] == 1:  
                dct["sub_question_id"] = sub_question[0]
                dct["count"] = row["count"]
            
        # if there is no value that equals 1, dont append empty dict
        if dct != {}:
            lst.append(dct)
        dct  = {}
    
    return sorted(lst, key=lambda d: d['count']) 

def numeric_transform(db, question_id):
    
    # Value is not null is required for this table
    result = sql_query(db, f"""
    SELECT COUNT(value) as count, value FROM q_response_v1 WHERE question_item_id = '{question_id}' AND value IS NOT NULL GROUP BY value ORDER BY count
    """)
    
    lst = []
    
    for row in result:
        dct = {}
        dct["value"] = int(row["value"])
        dct["count"] = row["count"]
        lst.append(dct)

    return lst

def matrix_transform(db, question_id):
    
    sub_questions = sql_query(db, f"""
    SELECT subquestion_id FROM q_response_v1 WHERE question_item_id IN 
        (
        SELECT question_item_id from q_response_v1 where question_item_id = '{question_id}'
        ) 
    GROUP BY subquestion_id
    """)
    
    lst = []
    dct  = {}
    
    for sub_question in sub_questions:
        query_string_value_counts_multiple_choice = f'''
        SELECT value, COUNT(value) FROM q_response_v1 WHERE subquestion_id = '{sub_question[0]}' AND value IS NOT NULL GROUP BY value
        '''
        
        result = single_choice_transform(db, query_string_value_counts_multiple_choice, value_label=False)
        
        dct["sub_question_id"] = sub_question[0]
        lst2 = []
        
        for row in result: 
            dct2 = {}
            dct2["value"] = row["value"]
           
            dct2["count"] = row["count"]
            
            lst2.append(dct2)
        
        dct["value_counts"] = lst2
        
        lst.append(dct)
        dct  = {}
    
    return sorted(lst, key=lambda d: d['sub_question_id']) 