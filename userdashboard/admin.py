# users/admin.py
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


# Provides the admin page with the custom user model and registers all other models into it. ###

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'userLevel', 'sub_since', 'sub_until']
    fieldsets = (
        (('User'), {'fields': ('username', 'password', 'email', 'userLevel', 'sub_since', 'sub_until', 'date_joined', 'last_login')}),
        (('Permissions'), {'fields': ('is_active','is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (('User'), {'fields': (
        'username', 'email', 'password1', 'password2', 'userLevel', 'sub_since', 'sub_until', 'date_joined', 'last_login')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )


admin.site.register(Permission)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Payment_Crypto)
admin.site.register(Payment_Fiat)
admin.site.register(Currency_Value)
admin.site.register(ChangeLog)
admin.site.register(BugReport)
admin.site.register(Coin)
admin.site.register(Payment_Error)
admin.site.register(Pricing_Fiat)
admin.site.register(UsedCoupon)
admin.site.register(StripeWebhook)
admin.site.register(Invoice)
admin.site.register(ActiveSubscription)

# Content Models
admin.site.register(Beam)
admin.site.register(BlockchainEvent)
admin.site.register(BlockchainNew)
admin.site.register(ArtificialIntelligence)
admin.site.register(TechnicalAnalysi)
admin.site.register(TokenWatchlist)
admin.site.register(BeamsComment)
admin.site.register(BlockchainEventsComment)
admin.site.register(BlockchainNewsComment)
admin.site.register(ArtificialIntelligenceComment)
admin.site.register(TechnicalAnalysisComment)
admin.site.register(TokenWatchlistComment)
