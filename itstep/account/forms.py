from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    # email = forms.EmailField(help_text="Required email")

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']
        labels = {"email": "Required email"}
        help_texts = {"email": "Please enter a valid email address."}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email


########### Extending the user model

class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Робимо поле username нередагованим
        self.fields['username'].disabled = True

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']


    def clean_email(self):
        data = self.cleaned_data['email']
        User = get_user_model()
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date',  'placeholder': 'Select your birth date'}
            ),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

