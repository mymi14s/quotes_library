import sqlite3, os
from sqlite3 import Error
from .utils import query_db


def get_quotes(category=None, author=None, count=1, random=False):
    """
    Return a list of all users.
    """
    conditions = " WHERE 1=1 "
    if(category):
        conditions += f""" AND category LIKE "%{category}%" """
    elif(author):
        conditions += f""" AND author LIKE "%{author}%" """
    if random:
        conditions +=  """ ORDER BY RANDOM() """
    elif not (category and author) and random:
        conditions +=  """ ORDER BY RANDOM() """
    conditions += f""" LIMIT {count} """
    sql = """
        SELECT author, category, quote FROM Quote
        {conditions}
    """.format(conditions=conditions)
    return query_db(sql)