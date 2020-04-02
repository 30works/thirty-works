from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import MyUserCreationForm, UserUpdateForm, UserProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import Day
from django.forms import ValidationError
import copy


# Create your views here.
def register(request):
    days = Day.objects.all()
    if len(days) < 1:
        if request.method == 'POST':
            # form = UserCreationForm(request.POST)
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account created for {}'.format(username))
                # and send the user back to homepage
                return redirect('blog-home')
                # and send user to login page
                # return redirect('login')
        else:
            # form = UserCreationForm()
            form = MyUserCreationForm()
        return render(request, 'users/register.html', {'form': form})
    else:
        return redirect('home')


class MyUserUpdateForm(UserUpdateForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request') # get request from kwargs, but don't pass that kwarg to super
        super().__init__(*args, **kwargs)

    def clean(self):
        print('HUNTING FOR DISALLAWED CHARS')
        # current_user = self.user  # from init
        DISALLOWED_CHARS = r" /'!£$%^&*()+=~#:\\\""
        username = self.data['username']
        if any(elem in username for elem in DISALLOWED_CHARS):
            print('Found a disallowed char!!!\n')
            cleaned_username = copy.deepcopy(username)
            for char in DISALLOWED_CHARS:
                cleaned_username = cleaned_username.replace(char, '')
            self.cleaned_data['username'] = cleaned_username
            raise ValidationError("Invalid character in username")
        super().clean()


@login_required
def profile(request):
    if request.method == 'POST':
        # u_form = UserUpdateForm(request.POST, instance=request.user)
        u_form = MyUserUpdateForm(request.POST, instance=request.user, request=request)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid character in username, please use only alphanumeric characters and underscores')



    else:
        print('NOT a POST method')
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)