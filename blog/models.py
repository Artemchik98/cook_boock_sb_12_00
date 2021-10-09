from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# Create your models here.
from django.utils import timezone
from slugify import slugify
from taggit.managers import TaggableManager


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250,
                             verbose_name='Название поста')
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts',
                               verbose_name='Автор')
    short_description = models.CharField(
        max_length=400,
        verbose_name='Краткое описание')
    publish = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата публикации')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft',
                              verbose_name='Статус публикации')
    image = models.ImageField(
        upload_to='product_images/',
        blank=False,
        verbose_name='Изображение')
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)


def save_image(instance, filename):
    post_id = instance.post.id
    return 'gallery_images/{}/{}'.format(
        post_id, filename
    )


class PostPoint(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             default=None,
                             verbose_name='Пост этапа готовки')

    post_point_header = models.CharField(max_length=250,
                                   default='HEADER',
                                   verbose_name='Шапка этапа готовки')

    post_point_text = models.TextField(
        verbose_name='Текст этапа готовки')
    post_point_image = models.ImageField(
        upload_to=save_image, blank=True,
        verbose_name='Изображение этапа готовки'
    )

    class Meta:
        verbose_name = 'Этап готовки'
        verbose_name_plural = 'Этапы готовки'


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comment',
                             verbose_name='Комментарии')
    name = models.CharField(max_length=80,
                            verbose_name='Имя')
    email = models.EmailField()
    body = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания комментария')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления комментария')
    active = models.BooleanField(
        default=True, verbose_name='Статус')

    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return 'Комментарий написан {} о {}' \
            .format(self.name, self.post)
