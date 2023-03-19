from urllib import request
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post

# Create your views here.

coins = [
    {
        'name': 'Bitcoin',
        'price': "{:,}".format(19438),
        'diff': 1.96,
        'cap': "{:,}".format(371625886829)
    },
    {
        'name': 'Ethereum',
        'price': "{:,}".format(1321),
        'diff': 0.09,
        'cap': "{:,}".format(161613832854),
    },
    {
        'name': 'Tether',
        'price': "{:,}".format(1),
        'diff': 0,
        'cap': "{:,}".format(67951030165)
    }
]


def home(request):
    context = {
        'coins': coins,
        'posts': Post.objects.all()
    }
    return render(request, 'base/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'base/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    extra_context = {'coins': coins}
    paginate_by = 4


class UserListView(ListView):
    model = Post
    template_name = 'base/user_posts.html'
    context_object_name = 'posts'
    extra_context = {'coins': coins}
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  
def about(request):
    return render(request, 'base/about.html', context={'coins': coins})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return True if post.author == self.request.user else False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'base/post_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return True if post.author == self.request.user else False