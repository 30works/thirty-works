from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# # Create your views here.

# function-based views

# def home(request):
#     # return HttpResponse("<h1>hullo :)</h1>")
#     ontext = {
#         # "posts": DUMMY_CONTENT
#         "posts": Post.objects.all()
#     }
#     return render(request, "blog/home.html", context=ontext)

# class-based views

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    # by default ListView will want to loop over a variable called `object_list`, but we called it `posts`
    # in the dictionary above
    context_object_name = 'posts'
    ordering = ['date_posted']  # oldest to newst
    # ordering = ['-date_posted'] # newest to oldest

    # queryset = Post.objects.all()
    # paginator = Paginator(queryset, paginate_by)

    paginate_by = 10


class PostDetailView(DetailView):
    model = Post


class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # get user from kwargs, but don't pass that kwarg to super
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ['title', 'content']

    def clean(self):
        current_user = self.user  # from init
        # if Post.objects.filter(author=current_user, date_posted=timezone.now().today()).exists():
        print('timezone.now().date()='.format(timezone.now().date()))
        print('current_user={}'.format(current_user))
        # print(Post.objects.filter(author=current_user, date_posted=timezone.now().date()))
        if Post.objects.filter(author=current_user, date_posted__date=timezone.now().date()).exists():
            # messages.error(current_user, 'You already submitted something today!')
            print('User {} was forbidden from posting again today'.format(self.user))
            raise forms.ValidationError("You already submitted something today")
        else:
            print('This is the users first submission ofthe day 1!!!!')
        super().clean()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'content']
    form_class = CreatePostForm

    def get_form_kwargs(self):
        """ add user to form kwargs """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        '''
        Assign the currently logged-in user as the author of this post
        '''
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        '''
        Assign the currently logged-in user as the author of this post
        '''
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        '''
        Check that the currently logged-in user is the author of the post attempting to be updated
        '''
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        '''
        Check that the currently logged-in user is the author of the post attempting to be updated
        '''
        post = self.get_object()
        return self.request.user == post.author


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    # by default ListView will want to loop over a variable called `object_list`, but we called it `posts`
    # in the dictionary above
    context_object_name = 'posts'
    ordering = ['date_posted']  # oldest to newst

    # ordering = ['-date_posted'] # newest to oldest

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def about(request):
    # return HttpResponse()
    return render(request, "blog/about.html", context={'title': 'A nice little title for the about page'})


from django.shortcuts import render

# Create your views here.
