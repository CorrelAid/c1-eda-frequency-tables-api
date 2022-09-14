from sqlacodegen.codegen import CodeGenerator
from sqlalchemy import select, text
import io

def generate_model(engine, metadata, outfile = None):
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.render(outfile)
    

def sql_query(db, query):
    """ 
    Executes a SQL query inputted as string on the server
    """
    return db.execute(text(query))

def sql_to_dict(db, query):
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

def sql_to_single(db, query):
    """ 
    Given a valid sql query result containing a single result(one row) returns the result as the type it was saved in db as.
    """
    result = sql_query(db, query).all()
    return result[0]["count"]