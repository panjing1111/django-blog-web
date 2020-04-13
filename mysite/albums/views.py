from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
from django.utils import timezone
from .forms import UploadPhotoForm
import time
import os
# Create your views here.


def upload_photo(request):
    # '''上传图片'''
    if request.method == "POST":
        upload_photo_form = UploadPhotoForm(request.POST, request.FILES)
        # 判断表单值是否合法
        if upload_photo_form.is_valid():
            new_photo = upload_photo_form.save(commit=False)
            file_obj = request.FILES.get('body')
            file_name = 'images/' + '_' + str(int(time.time())) + '.' + file_obj.name.split('.')[-1]  # 构造文件名以及文件路径
            new_photo.title = request.POST['title']
            new_photo.author =request.user
            new_photo.save()
            print(os.getcwd())
            with open(os.path.join('/Users/z/django-blog-web/mysite/media/',file_name), 'wb+') as f:
                f.write(file_obj.read())
            return HttpResponse('OK')

    else:
        photo = UploadPhotoForm()
        return render(request, 'albums/photo.html', context={'photo':photo})