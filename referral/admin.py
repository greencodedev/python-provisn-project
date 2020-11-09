from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Referral)
#admin.site.register(ReferralReward)
admin.site.register(SignedUpUserReferral)
admin.site.register(OpenPayout)
