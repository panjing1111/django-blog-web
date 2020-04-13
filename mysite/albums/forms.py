from django import forms
from .models import PersonalPhoto


class UploadPhotoForm(forms.ModelForm): # ModelForm得实例对象支持save操作，Form不支持
    '''上传图片时的表单'''
    class Meta:
        model = PersonalPhoto
        # 出现表单后要求填写的字段
        fields = ('title', 'body')
