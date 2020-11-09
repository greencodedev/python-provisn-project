from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TelegramAccountWrapper)
admin.site.register(TelegramActiveUsersBroadcast)
admin.site.register(TelegramActiveUsersChat)
admin.site.register(ContentCoinDesk)
