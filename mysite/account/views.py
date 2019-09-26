from django.shortcuts import render
from .forms import RegistrationForm, UserProfileForm
from django.http import HttpResponse
# Create your views here.



def register(request):
    if request.method == 'GET':
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, 'account/register.html', {"form":user_form, "profile":userprofile_form})
    else:
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        print(user_form.is_valid())
        print(userprofile_form.is_valid())
        if user_form.is_valid() and userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponse("successfully")
        else:
            return HttpResponse('sorry, you can not register')
