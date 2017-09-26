from django import forms
# from ..models import
#设置表单类的文件

class LoginForm(forms.Form):
    username = forms.CharField(max_length=12, min_length=6,
                               required=True,
                               error_messages={"required":"用户账号不能为空",
                               'invalid':'格式错误'},
                               widget=forms.TextInput(attrs={"class":"c"}))
    #"class":"c"  这个可以用来添加样式
    #表单类成功，密码长度，使用密文
    passwd = forms.CharField(max_length=16,min_length=6,
                             widget=forms.PasswordInput)

# class registerForm(forms.Form):
#     class Meta:
#         model =
