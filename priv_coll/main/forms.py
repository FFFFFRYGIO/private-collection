from django import forms


class AddBooks(forms.Form):
    intitle = forms.CharField(label='In the title', max_length=200, required=False)
    inauthor = forms.CharField(label='In the authors', max_length=200, required=False)
    inpublisher = forms.CharField(label='In the publisher', max_length=200, required=False)
    subject = forms.CharField(label='In the category list', max_length=200, required=False)
    isbn = forms.CharField(label='Exact ISBN number', max_length=200, required=False)
    lccn = forms.CharField(label='In the Library of Congress Control Number', max_length=200, required=False)
    oclc = forms.CharField(label='In the Online Computer Library Center number', max_length=200, required=False)
