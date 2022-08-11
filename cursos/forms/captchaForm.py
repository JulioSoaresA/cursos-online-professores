from django import forms
from captcha.fields import CaptchaField


class CaptchaForm(forms.Form):
    token = forms.CharField(max_length=32)
    captcha = CaptchaField()