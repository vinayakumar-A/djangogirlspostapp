from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from my_app.models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):

    posts = Post.objects.filter(published_at__lte=timezone.now()).order_by('published_at')
    paginator = Paginator(posts, 5) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj}
    return render(request, 'my_app/post_list.html', context)


def post_detail(request, pk):

    post = get_object_or_404(Post , pk=pk)
    context = {'post':post}
    return render(request, 'my_app/post_detail.html', context)


def post_new(request):

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_at = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()
    context = {'form':form}
    return render(request, 'my_app/new_post.html', context)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_at = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    context = {'form':form}
    return render(request, 'my_app/new_post.html', context)