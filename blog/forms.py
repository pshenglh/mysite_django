from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=40,
                               required=True, error_messages={'required':'请输入用户名'})
    password = forms.CharField(label='密码', max_length=30,
                               required=True, error_messages={'required':'请输入密码'})

class SignUpForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=40)
    email = forms.EmailField()
    password = forms.CharField(label='密码', max_length=30)
    password1 = forms.CharField(label='确认密码', max_length=30)

class BlogForm(forms.Form):
    title = forms.CharField(label='标题', max_length=50)
    body_text = forms.Textarea()

class CommentForm(forms.Form):
    com_text = forms.CharField(label='评论')