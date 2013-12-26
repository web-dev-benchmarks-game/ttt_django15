from django import forms
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class RegisterForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', max_length=40, error_messages={
        'invalid': "Usernames must contain only letters, numbers, and the underscore.",
    })
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']):
            raise forms.ValidationError("A user with this name already exists.")
        return self.cleaned_data['username']

class RegisterView(generic.edit.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    # Can't just use "reverse" here, since it gets evaluated at import time
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = User.objects.create_user(username,
                                        password=password)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)
