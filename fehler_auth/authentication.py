import pytz

import datetime as dtime
from datetime import datetime
from datetime import timedelta

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token")

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted")

        # This is required for the time comparison
        utc_now = datetime.now(dtime.timezone.utc)
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(minutes=2):
            raise exceptions.AuthenticationFailed("Token has expired")

        return token.user, token
