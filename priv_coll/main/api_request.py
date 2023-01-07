from requests import get


def generate_query(book_params: dict) -> str:
    """generate query based on parameters parsed by user"""

    query = ""

    for param in book_params:
        if not len(query):
            query += param + ":" + book_params[param]
        else:
            query += "+" + param + ":" + book_params[param]

    return query


def get_api_request(book_params: dict) -> dict:
    """creates request for google api and parses the response"""

    if not len(book_params):
        return {"error": -1}

    url = r"https://www.googleapis.com/books/v1/volumes"

    query = generate_query(book_params)
    params = {"q": query}
    response = get(url, params=params)
    response_dict = response.json()

    if response_dict["totalItems"]:
        return response_dict
    else:
        return {"error": -1}
