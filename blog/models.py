from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth .models import User
from django.urls import reverse
class Post(models.Model):
    STATUS_CHOICES=(
        ('draft','Draft'),
        ('published','Published'),
    )
    title=models.CharField(max_length=250,
               verbose_name='Название поста')
    slug=models.SlugField(max_length=250,
              unique_for_date='publish')
    author=models.ForeignKey(User,
             on_delete=models.CASCADE,
             related_name='blog_posts',
             verbose_name='Автор')
    short_description=models.CharField(
        max_length=400,
        verbose_name='Краткое описание')
    publish=models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата публикации')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')
    status=models.CharField(max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус публикации')
    image=models.ImageField(
        upload_to='product_images/',
        blank=False,
        verbose_name='Изображение')

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title
    #from django.urls import reverse

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                   args=[self.publish.year,
                         self.publish.month,
                         self.publish.day,
                         self.slug])

def save_image(instance,filename):
    post_id=instance.post.id
    return 'gallery_images/{}/{}'.format(
        post_id,filename
    )

class PostPoint(models.Model):
    post=models.ForeignKey(Post,
            on_delete=models.CASCADE,
            default=None)

    post_header=models.CharField(max_length=250,
                                 default='HEADER')

    post_point_text=models.TextField(
        verbose_name='Текст пункта')
    post_point_image=models.ImageField(
        upload_to=save_image,blank=True,
        verbose_name='Изображение пункта'
    )

