from django import forms


class AddBooks(forms.Form):
    intitle = forms.CharField(label="In the title", max_length=200, required=False)
    inauthor = forms.CharField(label="In the authors", max_length=200, required=False)
    inpublisher = forms.CharField(label="In the publisher", max_length=200, required=False)
    subject = forms.CharField(label="In the category list", max_length=200, required=False)
    isbn = forms.CharField(label="Exact ISBN number", max_length=200, required=False)
    lccn = forms.CharField(
        label="In the Library of Congress Control Number",
        max_length=200,
        required=False,
    )
    oclc = forms.CharField(
        label="In the Online Computer Library Center number",
        max_length=200,
        required=False,
    )


class AddNewBook(forms.Form):
    ISBN = forms.CharField(label="ISBN", max_length=13, required=True)
    title = forms.CharField(label="title", max_length=270, required=True)
    authors = forms.CharField(label="authors", max_length=110, required=False)
    publishedDate = forms.CharField(label="publishedDate", max_length=10, required=False)
    pageCount = forms.IntegerField(label="pageCount", required=False)
    thumbnail = forms.CharField(label="thumbnail", max_length=200, required=False)
    language = forms.CharField(label="language", max_length=10, required=False)
    cost = forms.FloatField(label="cost", required=False)


class EditBook(forms.Form):
    title = forms.CharField(label="title", max_length=270, required=True)
    authors = forms.CharField(label="authors", max_length=110, required=False)
    publishedDate = forms.CharField(label="publishedDate", max_length=10, required=False)
    pageCount = forms.IntegerField(label="pageCount", required=False)
    thumbnail = forms.CharField(label="thumbnail", max_length=200, required=False)
    language = forms.CharField(label="language", max_length=10, required=False)
    cost = forms.FloatField(label="cost", required=False)
