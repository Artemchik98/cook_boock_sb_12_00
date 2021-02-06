from django.urls import path
from . import  views

app_name='blog'
urlpatterns=[
    # path('',views.post_list,name='post_list'),
    path('',views.PostlistView.as_view(),name="post_list"),


    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,
         name='post_detail')
]
# templates/blog/post
# в папке blog создать base.html
# в папке post создать list.html и
#                      detail.html