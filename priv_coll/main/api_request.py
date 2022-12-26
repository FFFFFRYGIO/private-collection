from requests import get
from django.contrib import messages


def generate_query(book_params):
    # book_params is a dict with parameters to import book

    query = ''

    for param in book_params:
        if not len(query):
            query += param + ':' + book_params[param]
        else:
            query += '+' + param + ':' + book_params[param]

    return query


def get_api_request(book_params):
    if not len(book_params):
        # messages.add_message('No parameters to add books')
        return -1

    url = r'https://www.googleapis.com/books/v1/volumes'

    query = generate_query(book_params)
    params = {"q": query}
    response = get(url, params=params)
    response_dict = response.json()

    if response_dict['totalItems']:
        return response_dict
    else:
        return -1
