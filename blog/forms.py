from django import forms


class TagForm(forms.Form):
    name = forms.CharField(label="Title for tag",  # help_text="Enter your tag",
                           max_length=10)
    slug = forms.SlugField(max_length=31)

    def save(self, instance):
        instance.name = self.cleaned_data["name"]
        instance.slug = self.cleaned_data["slug"]
        instance.save()
        return instance





class RatingForm(forms.Form):
    RATING_CHOICES = [(i, str(i) ) for i in range(5, 0, -1)]  # Вибір з 5 до 1
    score = forms.ChoiceField(choices=RATING_CHOICES,
                              widget=forms.RadioSelect(attrs={'class': 'radio_1'}),
                              label="Score", )


# class RatingForm(forms.Form):
#     score = forms.IntegerField(min_value=1, max_value=5, widget=forms.HiddenInput())

# class ContactForm(forms.Form):
#     name = forms.CharField(max_length=100, required=True, label='Ваше ім\'я')
#     email = forms.EmailField(required=True, label='Ваша електронна пошта')
#     message = forms.CharField(widget=forms.Textarea, required=True, label='Ваше повідомлення')
#
#
# from django.shortcuts import render
# from .forms import ContactForm
#
# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             # Тут ви можете обробити дані форми, наприклад, надіслати електронний лист
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']
#             # Логіка для обробки даних (наприклад, надсилання електронної пошти)
#             return render(request, 'contact_success.html', {'name': name})
#     else:
#         form = ContactForm()
#
#     return render(request, 'contact.html', {'form': form})
