from flask import flash
from sqlalchemy import update, delete
from collections import namedtuple

from .api_request import get_api_request
from .models import Book


def add_books(book_params):
    response_dict = get_api_request(book_params)
    if response_dict == -1:
        return namedtuple('Result', ['errors', 'duplicates', 'success'])(-1, -1, -1)

    count_errors = 0
    count_duplicates = 0
    count_success = 0

    for info in response_dict['items']:
        vol = info['volumeInfo']
        curr_book = Book()

        # ISBN_13

        if not vol.get('industryIdentifiers'):  # No any ISBN identification
            count_errors += 1
            continue
        for isbn_elem in vol.get('industryIdentifiers'):
            if isbn_elem.get('type') == 'ISBN_13':
                curr_book.ISBN = isbn_elem.get('identifier')
        if curr_book.ISBN is None:  # No ISBN code
            count_errors += 1
            continue
        if Book.objects.filter(ISBN=curr_book.ISBN):  # ISBN already on the list
            count_duplicates += 1
            continue

        try:
            curr_book.title = vol.get('title', '<no title>')
        except TypeError:
            # print('no ISBN code!')
            count_errors += 1
            continue

        try:
            authors = vol.get('authors')[0]
            for i in range(1, len(vol.get('authors'))):
                authors += ', ' + vol.get('authors')[i]
            curr_book.authors = authors
        except TypeError:
            curr_book.authors = '<no authors>'

        try:
            curr_book.publishedDate = vol.get('publishedDate', None)
        except TypeError:
            curr_book.publishedDate = None

        try:
            curr_book.pageCount = vol.get('pageCount', None)
        except TypeError:
            curr_book.pageCount = None

        try:
            curr_book.thumbnail = vol.get('imageLinks').get('thumbnail', '<no thumbnail>')
        except (TypeError, AttributeError):
            curr_book.thumbnail = '<no thumbnail>'

        try:
            curr_book.language = vol.get('language', '<no language>')
        except TypeError:
            curr_book.language = '<no lan.>'

        curr_book.save()

    return namedtuple('Result', ['errors', 'duplicates', 'success'])(count_errors, count_duplicates, count_success)


def edit_book(book_target_isbn, book_config):
    wrong_inputs = []
    statements = []

    if 'pageCount' in book_config:
        pagecount_source = session.query(Book.pageCount).filter(Book.ISBN == book_target_isbn).first()[0]
        if not len(book_config['pageCount']):
            if pagecount_source:
                statements.append(update(Book).where(Book.ISBN == book_target_isbn
                                                     ).values(pageCount=None
                                                              ).execution_options(synchronize_session="fetch")
                                  )
            else:
                book_config.pop('pageCount')
        elif pagecount_source == int(book_config['pageCount']):
            book_config.pop('pageCount')
        else:
            statements.append(update(Book).where(Book.ISBN == book_target_isbn
                                                 ).values(pageCount=book_config['pageCount']
                                                          ).execution_options(synchronize_session="fetch")
                              )

    if not len(book_config):
        flash('No changes found')
        return False

    if 'title' in book_config:
        if len(book_config['title']) > 270:
            wrong_inputs.append('Title too long')
        elif len(book_config['title']) == 0:
            flash('Empty title')
            return False
        else:
            statements.append(update(Book).where(Book.ISBN == book_target_isbn
                                                 ).values(title=book_config['title']
                                                          ).execution_options(synchronize_session="fetch")
                              )

    if 'authors' in book_config:
        if len(book_config['authors']) > 100:
            wrong_inputs.append('Authors list too long')
        else:
            if len(book_config['authors']) == 0:
                book_config['authors'] = '<no authors>'
            statements.append(update(Book).where(Book.ISBN == book_target_isbn
                                                 ).values(authors=book_config['authors']
                                                          ).execution_options(synchronize_session="fetch")
                              )

    if 'publishedDate' in book_config:
        publisheddate_source = session.query(Book.publishedDate).filter(Book.ISBN == book_target_isbn).first()[0]
        if len(book_config['publishedDate']) > 10:
            wrong_inputs.append('Published date too long')
        else:
            if len(book_config['publishedDate']) == 0 or book_config['publishedDate'] == 'None':
                book_config['publishedDate'] = None
            if not (publisheddate_source is None and book_config['publishedDate'] is None):
                statements.append(update(Book).where(Book.ISBN == book_target_isbn
                                                     ).values(publishedDate=book_config['publishedDate']
                                                              ).execution_options(synchronize_session="fetch")
                                  )

    if 'thumbnail' in book_config:
        if len(book_config['thumbnail']) > 200:
            wrong_inputs.append('Thumbnail too long')
        else:
            if len(book_config['thumbnail']) == 0:
                book_config['thumbnail'] = '<no thumbnail>'
            statements.append(update(Book).where(Book.ISBN == book_target_isbn
                                                 ).values(thumbnail=book_config['thumbnail']
                                                          ).execution_options(synchronize_session="fetch")
                              )

    if 'language' in book_config:
        if len(book_config['language']) > 10:
            wrong_inputs.append('Language abbreviation too long')
        else:
            if len(book_config['language']) == 0:
                book_config['language'] = '<no lang.>'
            statements.append(update(Book).where(Book.ISBN == book_target_isbn
                                                 ).values(language=book_config['language']
                                                          ).execution_options(synchronize_session="fetch")
                              )

    if len(wrong_inputs):
        flash("Couldn't modify book with ISBN " + book_target_isbn)
        for mistake in wrong_inputs:
            flash(mistake)
        return False
    else:
        if len(statements):
            for stmt in statements:
                session.execute(stmt)
                session.commit()
            return True
        else:
            flash('No changes found')
            return False


def delete_book(book_isbn):
    del_book = (delete(Book).where(Book.ISBN == book_isbn))
    session.execute(del_book)
    session.commit()
    return True


def get_books():
    query = session.query(Book.ISBN, Book.title, Book.authors, Book.publishedDate,
                          Book.pageCount, Book.thumbnail, Book.language).order_by(Book.ISBN).all()
    books = []
    for book in query:
        book_dict = dict(zip(book_attributes, book))
        books.append(book_dict)

    return books


def get_book_by_isbn(book_isbn):
    query = session.query(Book.ISBN, Book.title, Book.authors, Book.publishedDate,
                          Book.pageCount, Book.thumbnail, Book.language).filter(Book.ISBN == book_isbn).first()
    book_dict = dict(zip(book_attributes, query))

    return book_dict
