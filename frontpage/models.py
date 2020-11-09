from django.db import models
from django.utils import timezone
from captcha.fields import ReCaptchaField

# Create your models here.
class SupportTicket(models.Model):
    byName = models.CharField(max_length=200)
    email_ticket = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=128, default="OPEN")
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    captcha = ReCaptchaField(label='')

    def __str__(self):
        return self.get_status() + ' (' + str(self.byName) + ') ' + ' @ ' + str(self.created_date)

    def get_status(self):
        return '[' + str(self.status) + ']'