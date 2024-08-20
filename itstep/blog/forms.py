from django import forms
from .models import Comment, Tag, Post
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




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'tags', 'category', 'image']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')

        if not tags:
            raise forms.ValidationError("Будь ласка, виберіть принаймні один тег.")

        # Додаткові перевірки, якщо потрібно
        if len(tags) > 5:  # Наприклад, обмежити до 5 тегів
            raise forms.ValidationError("Можна вибрати не більше 5 тегів.")

        return tags

