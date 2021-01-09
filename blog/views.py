from django.shortcuts import render,get_object_or_404


# Create your views here.
from .models import Post ,PostPoint
def post_list(request):
    posts=Post.objects.all()
    return  render(request,
           'blog/post/list.html',
           {'posts':posts})

def post_detail(request,year,
                month,day,post):
    post_object=get_object_or_404(Post,
                  slug=post,
                  publish__year=year,
                  publish__month=month,
                  publish__day=day)
    post_points=PostPoint.objects.filter(
        post=post_object)
    return  render(request,
               'blog/post/detail.html',
               {'post':post_object,
                'post_points':post_points})

