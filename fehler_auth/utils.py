from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        customized_response = {}
        customized_response["errors"] = {}
        print(response.data.items())
        for key, value in response.data.items():
            customized_response["errors"][key] = value[0]

        response.data = customized_response

    return response


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


token_generator = TokenGenerator()
