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
    if random or (not (category and author and random)):
        conditions +=  """ ORDER BY RANDOM() """
    elif not (category and author) and random:
        conditions +=  """ ORDER BY RANDOM() """
    conditions += f""" LIMIT {count} """
    sql = """
        SELECT author, category, quote FROM Quote
        {conditions}
    """.format(conditions=conditions)
    return query_db(sql)

def get_authors(count=0, random=False):
    """
    Return list of authors
    """
    conditions = " "
    if (random):
        conditions +=  """ ORDER BY RANDOM() """
    if(count>0):
        conditions += f""" LIMIT {count} """
    sql = """ SELECT DISTINCT author FROM Quote
        GROUP BY author
        {conditions}
    """.format(conditions=conditions)
    authors_dict = query_db(sql)
    if authors_dict.get('status_code') == 200 and len(authors_dict.get('data')):
        authors = [i['author'] for i in authors_dict['data']]
        authors_dict['data'] = authors
        return authors_dict
    return authors_dict


def get_categories(count=0, random=False):
    """
    Return list of Categories
    """
    conditions = " "
    if (random):
        conditions +=  """ ORDER BY RANDOM() """
    if(count>0):
        conditions += f""" LIMIT {count} """
    sql = """ SELECT DISTINCT category FROM Quote
        GROUP BY category 
        {conditions}
    """.format(conditions=conditions)

    category_dict = query_db(sql)
    if category_dict.get('status_code') == 200 and len(category_dict.get('data')):
        category = [i['category'] for i in category_dict['data']]
        category_dict['data'] = category
        return category_dict
    return category_dict