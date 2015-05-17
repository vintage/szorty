import uuid

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class Word(models.Model):
    name = models.CharField('Name', max_length=255, db_index=True, unique=True)
    created_at = models.DateTimeField('Create date', auto_now_add=True)
    updated_at = models.DateTimeField('Last update', auto_now=True)

    def __str__(self):
        return self.name


class Shortcut(models.Model):
    slug = models.SlugField('Slug field')
    target_url = models.URLField('Redirection URL')
    word = models.OneToOneField(Word, verbose_name='Matched word')
    redirection_count = models.PositiveIntegerField('Redirection count',
                                                    default=0)
    created_at = models.DateTimeField('Create date', auto_now_add=True)
    updated_at = models.DateTimeField('Last update', auto_now=True)

    class Meta:
        verbose_name = 'Redirection URL'
        verbose_name_plural = 'Redirection URLs'

    def __str__(self):
        return self.target_url

    def visited(self):
        self.redirection_count += 1

    def save(self, *args, **kwargs):
        self.slug = str(uuid.uuid4())

        return super(Shortcut, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shortcut_detail', args=[self.slug])

    def get_redirection_url(self):
        url = reverse('shortcut_redirect', args=[self.word.name])

        return '{}{}'.format(settings.SITE_URL, url)