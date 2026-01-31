import sqlite3, os
from sqlite3 import Error
try:
    from .utils import query_db
except ImportError:
    from utils import query_db


def get_quotes(category=None, author=None, count=1, random=False):
    """
    Return a list of quotes based on filtering criteria.
    """
    sql = "SELECT author, category, quote FROM Quote WHERE 1=1"
    params = []

    if category:
        sql += " AND category LIKE ?"
        params.append(f"%{category}%")
    if author:
        sql += " AND author LIKE ?"
        params.append(f"%{author}%")

    if random:
        sql += " ORDER BY RANDOM()"
    
    sql += " LIMIT ?"
    params.append(count)

    return query_db(sql, params)

def get_authors(count=0, random=False):
    """
    Return list of authors
    """
    sql = "SELECT DISTINCT author FROM Quote"
    params = []

    if random:
        sql += " ORDER BY RANDOM()"
    
    if count > 0:
        sql += " LIMIT ?"
        params.append(count)

    authors_dict = query_db(sql, params)
    if authors_dict.get('status_code') == 200 and authors_dict.get('data'):
        authors = [i['author'] for i in authors_dict['data']]
        authors_dict['data'] = authors
    return authors_dict


def get_categories(count=0, random=False):
    """
    Return list of Categories
    """
    sql = "SELECT DISTINCT category FROM Quote"
    params = []

    if random:
        sql += " ORDER BY RANDOM()"
    
    if count > 0:
        sql += " LIMIT ?"
        params.append(count)

    category_dict = query_db(sql, params)
    if category_dict.get('status_code') == 200 and category_dict.get('data'):
        category = [i['category'] for i in category_dict['data']]
        category_dict['data'] = category
    return category_dict