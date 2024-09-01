from django import forms
from django.core.mail import EmailMessage

from .models import Comment, Tag, Post
from django.core.exceptions import ValidationError


def validate_lowercase(value):
    if value.lower()!=value:
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
    name = forms.CharField(label='Title for tag', help_text="Enter your tag",
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         "placeholder": "Enter new tag"}),
                           # validators=[validate_lowercase]
                           )

    class Meta:
        model = Tag
        fields = ['name']

        # fields = "__all__"  # widgets = {"name": forms.TextInput(attrs={"placeholder": "-Enter new tag-"})}

    def clean_name(self):
        value = self.cleaned_data['name']
        return value.lower()

    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data.get("name")) < 3:
            self.add_error(None, "The total number of chars  must be 3 or greate.")


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['image'].required = False
        self.fields['category'].empty_label = "Оберіть категорію"
        self.fields['title'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'tags', 'category', 'image', "publish"]
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
            'publish': forms.DateTimeInput(attrs={'type': 'datetime-local'})}
        labels = {'title': 'Назва публікації', 'body': 'Текст публікації'}

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')

        if not tags:
            raise forms.ValidationError("Будь ласка, виберіть принаймні один тег.")

        # Додаткові перевірки, якщо потрібно
        if len(tags) > 5:  # Наприклад, обмежити до 5 тегів
            raise forms.ValidationError("Можна вибрати не більше 5 тегів.")

        return tags

    # валідація на рівні поля форми
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Заголовок повинен містити не менше 5 символів.")
        return title.title()

    def clean_body(self):
        content = self.cleaned_data.get('body')
        if len(content) < 10:
            raise forms.ValidationError("Зміст повинен містити не менше 10 символів.")
        return content

    # Загальна валідація на рівні форми
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("body")

        if title and content and title in content:
            raise forms.ValidationError("Зміст не може містити заголовок.")

    def send_email(self, request, msg):
        # data = self.cleaned_data
        msg_body = msg
        email = EmailMessage(
            subject='New Post Entry',
            body=msg_body,
            from_email='no-reply@example.com',
                reply_to=['no-reply@example.com'], cc=[], bcc=[], to=['q'], attachments=[], headers={}, )
        email.content_subtype = 'plain'
        email.send()
        print("ok")
