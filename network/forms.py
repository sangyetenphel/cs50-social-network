from django import forms

class PostForm(forms.Form):
    post = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label='')
