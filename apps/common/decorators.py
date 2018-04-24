from django.http import HttpResponseForbidden


def login_required(func):

    def wrapper(request, *args, **kwargs):
        if request.user is None:
            return HttpResponseForbidden("nope")
        return func(request, *args, **kwargs)

    return wrapper