from django import forms
from .models import Comment, Tag
from django.core.exceptions import ValidationError


def validate_lowercase(value):
    if value.lower() != value:
        raise ValidationError(f"{value} is not lowercase.")

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class TagForm(forms.ModelForm):
    name = forms.CharField(label='Title for tag',
                           help_text="Enter your tag",
                           widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Enter new tag"}),
                           # validators=[validate_lowercase]
                           )

    class Meta:
        model = Tag
        fields = ['name']

        # fields = "__all__"
        # widgets = {"name": forms.TextInput(attrs={"placeholder": "-Enter new tag-"})}

    def clean_name(self):
        value = self.cleaned_data['name']
        return value.lower()

    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data.get("name")) < 3:
            self.add_error(None, "The total number of chars  must be 3 or greate.")


