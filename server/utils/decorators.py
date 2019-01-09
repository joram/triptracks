from django.http import HttpResponseForbidden
from apps.accounts.models import User


def login_required(func):

    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_pub_id")
        request.user = User.objects.get(pub_id=user_id)
        if not user_id:
            return HttpResponseForbidden("nope. login required")
        return func(request, *args, **kwargs)

    return wrapper
