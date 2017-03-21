from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=40)
    password = forms.CharField(label='密码', max_length=30)

class SignUpForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=40)
    email = forms.EmailField()
    password = forms.CharField(label='密码', max_length=30)
    password1 = forms.CharField(label='确认密码', max_length=30)
