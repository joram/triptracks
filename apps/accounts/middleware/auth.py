from apps.accounts.models import User


def _get_user(request):
    pub_id = request.session.get("user_pub_id")
    if pub_id is None:
        return None
    users = User.objects.filter(pub_id=pub_id)
    if users.exists():
        return users[0]


class UserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = _get_user(request)
        response = self.get_response(request)
        return response