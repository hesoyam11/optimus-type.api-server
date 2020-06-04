from django.db import models

from users.models import User


class Exercise(models.Model):
    LOCALES = (
        ('enUS', 'en_US'),
        ('ukUA', 'uk_UA'),
        ('ruRU', 'ru_RU')
    )

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    locale = models.CharField(max_length=4, choices=LOCALES)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=4096)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
