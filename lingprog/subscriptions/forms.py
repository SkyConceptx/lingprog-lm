from django import forms

class SubscriptionForm(forms.Form):
    nome=forms.CharField(label='Nome')
    titulo=forms.CharField(label='Titulo')
    email=forms.EmailField(label='Email')
    resumo=forms.CharField(label='Resumo')
