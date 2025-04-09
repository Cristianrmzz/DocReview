from django import forms



class DocumentUploadForm(forms.Form):
    documents = forms.FileField(required=True)
    