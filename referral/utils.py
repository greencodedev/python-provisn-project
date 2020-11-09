from .models import Referral



def getUserReferralToken(User):
    from django.core.exceptions import ObjectDoesNotExist
    try:
        ref = Referral.objects.get(User=User).Token
    except (ObjectDoesNotExist):
        import secrets
        ref = secrets.token_urlsafe(24)
        NewModelToken = Referral(Token=ref, User=User)
        NewModelToken.save()
    return ref

def getUserReferralTokenByToken(Token):
    from django.core.exceptions import ObjectDoesNotExist
    try:
        ref = Referral.objects.get(Token=Token)
    except (ObjectDoesNotExist):
        return None
    return ref