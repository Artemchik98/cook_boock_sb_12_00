from django.urls import path
from . import  views
from django.contrib.auth import views as \
    auth_views
app_name='blog'
urlpatterns=[
    path('',views.post_list,name='post_list'),
    path('tag/<slug:tag_slug>/',views.post_list,name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
    path('<int:post_id>/share/',views.post_share,name='post_share'),

    path('login/',auth_views.LoginView.as_view(),
         name='login'),
    path('logout/',auth_views.LogoutView.as_view(),
         name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('post-add/',views.post_add,name='post_add')
]
