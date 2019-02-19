from django.http import HttpResponseForbidden
from apps.accounts.models import User
import datetime
from functools import wraps
import json


class UnnamedGraphqlQueryException(Exception):
    pass


def timed_calls(view_func):

    def wrapped_view(*args, **kwargs):
        start = datetime.datetime.now()
        request = args[0]
        query = json.loads(request.body).get("query")
        name = query.split("{")[0].replace("query", "").strip()

        if name == "":
            raise UnnamedGraphqlQueryException()

        resp = view_func(*args, **kwargs)

        end = datetime.datetime.now()
        delta = end - start

        print(f"'{name}' took {delta.microseconds/1000}ms")
        return resp

    return wraps(view_func)(wrapped_view)


def login_required(func):

    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_pub_id")
        request.user = User.objects.get(pub_id=user_id)
        if not user_id:
            return HttpResponseForbidden("nope. login required")
        return func(request, *args, **kwargs)

    return wrapper
