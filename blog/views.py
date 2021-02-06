from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
from .models import Post ,PostPoint

from django.views.generic import ListView

class PostlistView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# def post_list(request):
#     object_list = Post.objects.all()
#     paginator = Paginator(object_list, 1)  # Выводи по одному обьекту на страницу
#     page = request.GET.get('page')
#
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, 'blog/post/list.html', {'page': page,
#                                                    'posts': posts})



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

from .forms import EmailPostForm
def post_share(request,post_id):
    post=get_object_or_404(Post,
                       id=post_id,
                       status='published')
    if request.method=='POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
    else:
        form=EmailPostForm()
    return render(request,
                  'blog/post/share.html',
                  {'post':post,
                   'form':form})


