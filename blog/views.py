from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
from .models import Post ,PostPoint
def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 1)  # Выводи по одному обьекту на страницу
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts})



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

