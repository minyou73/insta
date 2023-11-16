from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-id')

    context = {
        'posts':posts,
    }

    return render(request, 'index.html', context)


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    
    else:
        form = PostForm()

    context={
        'form':form,
    }
    return render(request, 'form.html', context)


@login_required
def likes(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    #이미 좋아요 버튼을 누른경우
    # if post in user.like_posts.all():
    if user in post.like_users.all():
        post.like_users.remove(user)
    # 좋아요 버튼을 아직 안누른경우
    else:
        post.like_users.add(user)
        # user.like_posts.add(post)


    return redirect('posts:index')

# def detail(request, id):


from django.http import JsonResponse

def likes_async(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False
    else:
        post.like_users.add(user)
        status = True

    context = {
        'status': status,
        'count' : len(post.like_users.all())
    }

    return JsonResponse(context)



def detail(request, id):
    post = Post.objects.get(id=id)
    form = CommentForm()

    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'detail.html', context)


def comment_create(request, post_id):
    form = CommentForm(request.POST)

    if form.is_valid():
        # form을 저장 => 추가로 넣어야 하는 데이터를 넣기 위해서 저장 멈춰!
        comment = form.save(commit=False)
        
        comment.post_id = post_id
        comment.save()


        return redirect('posts:detail', id=post_id)