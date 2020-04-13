from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
from django.utils import timezone
from .models import PersonalPhoto
from .forms import UploadPhotoForm
import time
import os
# Create your views here.


def upload_photo(request):
    # '''上传图片'''
    if request.method == "POST":
        photo = UploadPhotoForm(request.POST, request.FILES)
        # 判断表单值是否和法
        if photo.is_valid():
            author = request.user
            print(request.POST)
            title = request.POST['title']
            file_obj = request.FILES.get('body')
            file_name = 'images/' + '_' + str(int(time.time())) + '.' + file_obj.name.split('.')[
                -1]  # 构造文件名以及文件路径
            upload_time = models.DateTimeField(default=timezone.now)  # 照片上传时间
            personal_photo = PersonalPhoto(title=title, author=author, body=file_name, upload_time=upload_time)
            print(personal_photo)
            with open(os.path.join('/Users/z/django-blog-web/mysite/media/',file_name), 'wb+') as f:
                f.write(file_obj.read())
            return HttpResponse('OK')

    else:
        photo = PersonalPhoto()
        return render(request, 'albums/photo.html', context={'photo':photo})