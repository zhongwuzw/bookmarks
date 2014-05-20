#coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import re
class RegistrationFrom(forms.Form):
    username = forms.CharField(label = '用户名',max_length = 30)
    email = forms.EmailField(label = '电子邮箱')
    password1 = forms.CharField(
                                label = '密码',
                                widget = forms.PasswordInput()
                                )
    password2 = forms.CharField(
                                label = '请再输入密码',
                                widget = forms.PasswordInput()
                                )
    
    #使用了form的validator，函数名需固定为clean_fieldname
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$',username):
            raise forms.ValidationError('用户名只能由字母或下划线组成')
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('用户名已经存在')
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data :
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('密码不匹配')
    
class BookMarkSaveForm(forms.Form):
    url = forms.URLField(
                         label = '输入网址',
                         widget = forms.TextInput(attrs={'size':64})
                         )
    title = forms.CharField(
                         label = '标题',
                         widget = forms.TextInput(attrs={'size':64})
                         )
    tags = forms.CharField(
                         label = '输入标签',
                         required = False,
                         widget = forms.TextInput(attrs={'size':64})
                         )
    