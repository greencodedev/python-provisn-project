from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)

    @property
    def get_html_url(self):
        url = reverse('userdashboard:DetailsEvents', args=(self.id,))
        return f'<a href="{url}"> <div class="event">{self.title}</div> </a>'
