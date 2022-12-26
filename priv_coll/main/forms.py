from django import forms

key_words = ['intitle', 'inauthor', 'inpublisher', 'subject', 'isbn', 'lccn', 'oclc']


class AddBooks(forms.Form):
    intitle = forms.CharField(label="intitle", max_length=200, required=False)
    inauthor = forms.CharField(label="inauthor", max_length=200, required=False)
    inpublisher = forms.CharField(label="inpublisher", max_length=200, required=False)
    subject = forms.CharField(label="subject", max_length=200, required=False)
    isbn = forms.CharField(label="isbn", max_length=200, required=False)
    lccn = forms.CharField(label="lccn", max_length=200, required=False)
    oclc = forms.CharField(label="oclc", max_length=200, required=False)
