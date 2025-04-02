from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import BlogPost, Category, Comment
from .forms import BlogPostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blogs/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        # Filter to show only approved and published posts that are not featured
        queryset = BlogPost.objects.filter(is_approved=True, is_published=True, is_featured=False)

        # Check if a category_slug is passed in the URL, and filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add all categories to the context for filtering by category in the template
        context['categories'] = Category.objects.all()

        # Add featured posts to the context (approved, published, and featured)
        context['featured_posts'] = BlogPost.objects.filter(
            is_featured=True, is_approved=True, is_published=True
        )[:3]  # Limiting the number of featured posts to 3

        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context
    
    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj


from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import BlogPost
from .forms import BlogPostForm


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogs/blog_create.html'

    def form_valid(self, form):
        # Set the author to the current user
        form.instance.author = self.request.user
        # Set the post as 'not approved' and 'not published' initially
        form.instance.is_approved = False
        form.instance.is_published = False

        # Show success message
        messages.success(self.request,
                         'Your blog post has been created successfully! It will be displayed after approval by the Books for All team.')

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the detail page of the newly created blog post
        return reverse('blog_detail', kwargs={'slug': self.object.slug})


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogs/blog_update.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Your blog post has been updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('blog_detail', kwargs={'slug': self.object.slug})

def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
    
    return redirect('blog_detail', slug=slug)