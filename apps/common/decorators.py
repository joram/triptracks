from django.http import HttpResponseForbidden


def login_required(func):

    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_pub_id")
        if not user_id:
            return HttpResponseForbidden("nope. login required")
        return func(request, *args, **kwargs)

    return wrapper
