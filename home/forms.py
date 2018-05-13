from django import forms

# class HomeForm(forms.Form):
#     post = forms.CharField()
from home.models import Post


class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write some post...'
        }
    ))

    class Meta:
        model = Post
        fields = ('post',)


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput()
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput()
    )
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message'
    )
    source = forms.CharField(
        max_length=50,
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')

        if not name and not email and not message:
            raise forms.ValidationError('You have to write something')
