from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
from .models import Post ,PostPoint,Comment

from django.views.generic import ListView
from .forms import CommentForm
from django.db.models import Count

from taggit.models import Tag
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,
                    username=cd['username'],
                    password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse(
                        'Успешная авторизация')
                else:
                    return HttpResponse(
                        'Аккаунт заблокирован')
            else:
                return HttpResponse(
                    'Неверные данные')
    else:
        form=LoginForm()
    return render(request,
          'blog/account/login.html',
                  {'form':form})

@login_required
def post_list(request,tag_slug=None):
    object_list = Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(
            tags__in=[tag])
    paginator = Paginator(object_list, 3)  # Выводи по одному обьекту на страницу
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag':tag})


@login_required
def post_detail(request,year,
                month,day,post):
    post_object=get_object_or_404(Post,
                  slug=post,
                  publish__year=year,
                  publish__month=month,
                  publish__day=day)
    post_points=PostPoint.objects.filter(
        post=post_object)
    comments=post_object.comment.filter(
        post=post_object)
    new_comment=None
    if request.method=='POST':
        comment_form=CommentForm(
            data=request.POST)
        if comment_form.is_valid():
            cd= comment_form.cleaned_data
            new_comment=Comment(
                post=post_object,
                name=cd['name'],
                email=cd['email'],
                body=cd['comment'])
            new_comment.save()
    else:
        comment_form=CommentForm()
    post_tags_ids=post_object.tags.values_list(
        'id',flat=True)
    similar_posts=Post.objects.filter(
        tags__in=post_tags_ids,
        status='published').exclude(
        id=post_object.id)
    similar_posts=similar_posts.annotate(
        same_tags=Count('tags')).order_by(
        '-same_tags','-publish')[:4]
    return  render(request,
               'blog/post/detail.html',
               {'post':post_object,
                'post_points':post_points,
                'similar_posts':similar_posts,
                'comments':comments,
                'new_comment':new_comment,
                'comment_form':comment_form})




from .forms import EmailPostForm
from django.core.mail import send_mail

@login_required
def post_share(request,post_id):
    post=get_object_or_404(Post,
                       id=post_id,
                       status='published')
    sent=False
    if request.method=='POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(
                post.get_absolute_url())
            subject='''{} {} рекомендует вам
прочитать {}'''.format(cd['name'],cd['email'],
                       post.title)
            message='''Прочитай "{}" на сайте {}
комментарий: "{}" 
отправитель: {}'''.format(post.title,post_url,
                    cd['comments'],cd['name'])

            send_mail(subject,message,
                  'admin@myblog.com',
                  [cd['to']])
            sent=True

    else:
        form=EmailPostForm()
    return render(request,
                  'blog/post/share.html',
                  {'post':post,
                   'form':form,
                   'sent':sent})


@login_required
def dashboard(request):
    return render(request,'blog/account/dashboard.html')
