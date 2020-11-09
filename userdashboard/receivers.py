import decimal

from django.dispatch import receiver
from cryptapi.signals import payment_complete, payment_received
from userdashboard.accounts import UserMethods
from .models import Payment_Crypto
from django.contrib.auth import get_user_model
from django.utils import timezone


class PaymentCryptoReceiver:

    @receiver(payment_received)
    def payment_notification(order_id, payment, value, **kwargs):
        paymentObject = Payment_Crypto.objects.get(auto_increment_id=payment.request.order_id)
        paymentObject.payment_received = True

    @receiver(payment_complete)
    def payment_received(order_id, payment, value, **kwargs):
        print("############################################################")
        print("Payment Complete. Start Checking...!")
        print("############################################################")
        try:
            print("val: " + str(value))
            if payment.request.provider.coin == 'btc':
                checkValue = decimal.Decimal(value) * decimal.Decimal(10 ** -8)
            elif payment.request.provider.coin == 'eth':
                checkValue = decimal.Decimal(value) * decimal.Decimal(10 ** -18)
            else:
                print('Payment verification error: ' + payment.provider.coin)
                return
            print("Checking Value: " + str(checkValue))
            print(type(payment))
            print(payment)
            print(type(kwargs))
            print(kwargs)

            paymentObject = Payment_Crypto.objects.filter(value=checkValue, payment_done=False).latest('requested_at')
            print('PaymentObject retrieved successful')
        except Exception as exc:
            error_msg = "Error checking if cost accepted!: \n" + str(exc) + "\n\n"
            print(error_msg)
            from .models import Payment_Errors
            error = Payment_Errors(
                error_message=error_msg
            )
            error.save()
            return
        print('Cost Check done')
        paymentObject.add_log('Cost Check Successful!')
        print("Payment info:")
        try:
            payment_info = ''
            payment_info += "Confirmations: " + str(payment.confirmations) + '\n'
            payment_info += "value " + str(value) + '\n'
            payment_info += "####################" + '\n'
            payment_info += "KWARGS" + '\n'
            for key, value in kwargs.items():
                payment_info += "{0} = {1}".format(key, value) + '\n'
            payment_info += "####################" + '\n'
            payment_info += "value_paid: " + str(payment.value_paid)  + '\n'
            payment_info += "Requ. Order ID:" + str(payment.request.order_id)  + '\n'
            payment_info += "Requ. ID: " + str(payment.request.id)  + '\n'
            payment_info += "Requ. Status: " + payment.request.status  + '\n'
            payment_info += "Payment str: " + payment.__str__()  + '\n'
            payment_info += "Requ. str: " + payment.request.__str__()  + '\n'
            print(payment_info)
            paymentObject.add_log(payment_info)
        except Exception as exc:
            error_msg = "Couldnt get info correctly!\nTrying to ignore it!\n\n: " + exc + "\n\n"
            print(error_msg)
            from .models import Payment_Errors
            error = Payment_Errors(
                error_message=error_msg
            )
            error.save()
            paymentObject.add_log('EXCEPTION: ' + error_msg)
            pass

        print('Extending user subscription')
        paymentObject.add_log('Extending user subscription')
        try:
            user = paymentObject.user
            UserMethods.prolongUserSubscriptionByUserObject(user, timezone.timedelta(
                days=paymentObject.pricing.subscription_time_in_days))
            paymentObject.payment_done = True
            if paymentObject.coin == 'eth':
                paymentObject.pricing.amount_uses_eth += 1
            elif paymentObject.coin == 'btc':
                paymentObject.pricing.amount_uses_btc += 1
            paymentObject.pricing.save()
            paymentObject.save()
        except Exception as exc:
            error_msg = 'Account prolonging error!\n' + str(exc)
            print(error_msg)
            from .models import Payment_Errors
            error = Payment_Errors(
                error_message=error_msg
            )
            error.save()

        try:
            from userdashboard.models import UsedCoupon
            coupon = UsedCoupon(
                user=user,
                coupon=payment.pricing
            )
            coupon.save()
        except:
            pass

        try:
            from referral.models import SignedUpUserReferral
            refToken = SignedUpUserReferral.objects.get(User=user).RefToken
            if not refToken.ReferralSubscribers.filter(email=user.email).exists():
                refToken.AmountReferrals += 1
                refToken.check_reward()
                refToken.ReferralSubscribers.add(user)
                refToken.save()
            else:
                error_msg = 'User referral has already been gifted'
                print(error_msg)
                paymentObject.add_log(error_msg)
        except SignedUpUserReferral.DoesNotExist:
            pass
        except Exception:
            pass

        print('Sending confirmation mail...')
        from .utils import payment_confirmation_mail
        payment_confirmation_mail(user, str(paymentObject.value), str(paymentObject.pricing.subscription_time_in_days))

        add_log = "############################################################" + '\n'
        add_log += "If no error has occured: " + '\n'
        add_log += "Payment Successfully Done, Congratulations" + '\n'
        add_log += "############################################################"
        return

paymentReceiver = PaymentCryptoReceiver()
payment_complete.connect(paymentReceiver.payment_received)


