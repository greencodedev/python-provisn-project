from django.utils import timezone


class UserMethods:

    def prolongUserSubscriptionByRequest(request):
        print('run prolong user sub')
        request.user.userLevel = 2
        request.user.sub_since = timezone.now()
        request.user.sub_until = max(timezone.now() + timezone.timedelta(days=14), request.user.sub_until + timezone.timedelta(days=14))
        request.user.save()
        print("finished prolong user sub")

    def prolongUserSubscriptionByUserObject(userObject, timezoneTimedeltaObject):
        print('run prolong user sub')
        userObject.userLevel = 2
        userObject.sub_since = timezone.now()
        userObject.sub_until = max(timezone.now() + timezoneTimedeltaObject, userObject.sub_until + timezoneTimedeltaObject);
        userObject.save()
        print("finished prolong user sub")

    def extendUserTrialByUserObject(userObject, timezoneTimedeltaObject):
        print('run prolong user sub')
        userObject.userLevel = 1
        userObject.sub_since = timezone.now()
        userObject.sub_until = max(timezone.now() + timezoneTimedeltaObject, userObject.sub_until + timezoneTimedeltaObject);
        userObject.save()
        print("finished prolong user sub")