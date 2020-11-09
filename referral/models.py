from django.db import models
from django.contrib.auth import get_user_model
from userdashboard.accounts import UserMethods
from django.utils.timezone import timedelta


# Create your models here.
class Referral(models.Model):
    Token = models.CharField(max_length=128, unique=True)
    User = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    AmountSignups = models.IntegerField(default=0)
    AmountReferrals = models.IntegerField(default=0)
    ReferralSubscribers = models.ManyToManyField(get_user_model(), related_name='referred_users', blank=True)
    Amount_open_payoff = models.FloatField(default=0)
    Amount_paid_off = models.FloatField(default=0)
    To_be_paid_off = models.BooleanField(default=False)

    def check_reward(self):
        self.Amount_open_payoff = self.Amount_open_payoff + 10

    def __str__(self):
        return str(self.User)


class OpenPayout(models.Model):
    Holders_Name = models.CharField(max_length=256)
    Bank_Name = models.CharField(max_length=256)
    IBAN = models.CharField(max_length=34)
    SWIFT = models.CharField(max_length=256)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    reftoken = models.ForeignKey(Referral, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class SignedUpUserReferral(models.Model):
    RefToken = models.ForeignKey(Referral, on_delete=models.CASCADE)
    User = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class ReferralReward(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount_needed_referrals = models.IntegerField(default=1)
    rewarded_time_days = models.IntegerField(default=2)

    def __str__(self):
        return self.title
