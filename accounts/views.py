from PIL import Image
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from accounts.forms import RegistrationForm, EditProfileForm, UserExtraDataForm, LoginForm

from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    return render(request, 'accounts/home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('accounts:view_profile')
    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/login.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('accounts:home')
    else:
        form = RegistrationForm()

    context = {'form': form}

    return render(request, 'accounts/register.html', context)


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user

    context = {'user': user}

    return render(request, 'accounts/profile.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form_user = EditProfileForm(request.POST, instance=request.user)
        form_extra = UserExtraDataForm(request.POST, request.FILES, instance=request.user.userprofile)
        if all([form_user.is_valid(), form_extra.is_valid()]):
            form_user.save()

            if request.FILES.get('image'):
                form_extra = form_extra.save(commit=False)
                form_extra.image = request.FILES.get('image')
                form_extra.save()
            else:
                form_extra.save(update_fields=['description', 'city', 'website', 'phone'])
            return redirect('accounts:view_profile')
    else:
        form_user = EditProfileForm(instance=request.user)
        form_extra = UserExtraDataForm(instance=request.user.userprofile)

    context = {'form_user': form_user, 'form_extra': form_extra}
    return render(request, 'accounts/edit_profile.html', context)

# def edit_profile(request):
#     if request.method == 'POST':
#         form_user = EditProfileForm(request.POST, instance=request.user)
#         form_extra = UserExtraDataForm(request.POST, request.FILES, instance=request.user.userprofile)
#         if all([form_user.is_valid(), form_extra.is_valid()]):
#             form_user.save()
#
#             if request.FILES.get('image'):
#                 form_extra = form_extra.save(commit=False)
#                 image = Image.open(request.FILES.get('image'))
#                 size = (50, 50)
#                 image = image.resize(size, Image.ANTIALIAS)
#                 print(image)
#                 form_extra.image = image.path
#                 form_extra.save()
#             else:
#                 form_extra.save(update_fields=['description', 'city', 'website', 'phone'])
#             return redirect('accounts:view_profile')
#     else:
#         form_user = EditProfileForm(instance=request.user)
#         form_extra = UserExtraDataForm(instance=request.user.userprofile)
#
#     context = {'form_user': form_user, 'form_extra': form_extra}
#     return render(request, 'accounts/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            # bellow line help to remain logged in after change the password
            update_session_auth_hash(request, form.user)
            return redirect('accounts:view_profile')
        else:
            return redirect('accounts:change_password')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}

    return render(request, 'accounts/change_password.html', context)
