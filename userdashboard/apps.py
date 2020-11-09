from django.apps import AppConfig


class UserdashboardConfig(AppConfig):
    name = 'userdashboard'

    def ready(self):
        import userdashboard.receivers
        from userdashboard.receivers import PaymentCryptoReceiver