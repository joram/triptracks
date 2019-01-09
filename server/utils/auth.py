import json
from urllib2 import Request, urlopen, URLError

import settings


def auth_required(view):

    def wrapper():
        try:
            get_google_userinfo()
        except Unauthorized:
            return redirect(url_for('auth.login'))
        return view()

    return wrapper