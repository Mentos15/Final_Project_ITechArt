from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class ConfirenceList(models.Model):
    IT = 'IT'
    Since = 'Since'
    Football = 'Football'
    Ecology = 'Ecology'
    conf_list = [
        (IT, 'IT'),
        (Since, 'Since'),
        (Football, 'Football'),
        (Ecology, 'Ecology'),
    ]
    name = models.CharField(max_length=255)
    text = models.TextField()
    date_published = models.DateTimeField(auto_now_add=False)
    category = models.CharField(max_length=8, choices=conf_list, default=IT)
    img = models.ImageField(upload_to='static/images', null=True, blank=True)


class Records(models.Model):
    conference = models.ForeignKey(ConfirenceList, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)
