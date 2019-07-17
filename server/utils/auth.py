import datetime
from apps.accounts.models import SessionToken


def get_or_create_session_token(user):
    duration = datetime.timedelta(days=1)
    qs = SessionToken.objects.filter(user_pub_id=user.pub_id)
    if qs.exists():
        return qs[0], False
    token = SessionToken.objects.create(expires=datetime.datetime.now() + duration, user_pub_id=user.pub_id)
    return token, True
