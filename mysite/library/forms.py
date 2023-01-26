from django import forms
from django.contrib.auth.models import User

from .models import BookReview, Profilis, BookInstance


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reviewer')
        widgets = {'book': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')
        # widgets = {'username': forms.HiddenInput()}


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka', ]


class DateInput(forms.DateInput):
    input_type = 'date'


class UserBookCreateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ('book', 'reader', 'due_back')
        widgets = {'reader': forms.HiddenInput(), 'due_back': DateInput()}