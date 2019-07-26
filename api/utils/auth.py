import datetime
from apps.accounts.models import User, SessionToken


def get_or_create_session_token(user):
    duration = datetime.timedelta(days=1)
    qs = SessionToken.objects.filter(user_pub_id=user.pub_id)
    if qs.exists():
        return qs[0], False
    token = SessionToken.objects.create(expires=datetime.datetime.now() + duration, user_pub_id=user.pub_id)
    return token, True


def get_authenticated_user(info):
    session_token = info.context.META.get("HTTP_X_SESSION_TOKEN")
    qs = SessionToken.objects.filter(session_key=session_token, expires__gte=datetime.datetime.now())
    if qs.exists():
        token = qs[0]
        user_qs = User.objects.filter(pub_id=token.user_pub_id)
        if user_qs.exists():
            user = user_qs[0]
            return user
    return None
