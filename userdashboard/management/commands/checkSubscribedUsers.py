from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now


### This application checks all Trial or Subscription users, if their subscription is still running and
### sets it to userLevel 0 if necessary

class Command(BaseCommand):
    help = "Checks all users if their subscription has run out"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting PROVISN Database Update...")
        users = get_user_model().objects.all()
        for i in range(0, len(users)):
            if users[i].userLevel == 2 or users[i].userLevel == 1:
                if (users[i].sub_until < now()):
                    print(str(now()) + " ---  The subscription of " + users[i].__str__() + " userLevel: " + str(users[i].userLevel) + " has run out")
                    users[i].userLevel = 0
                    users[i].save()
        self.stdout.write("Done Subscription Check")
