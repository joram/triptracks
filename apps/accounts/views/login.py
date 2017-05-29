from django.conf import settings
from oauth2client import client, crypt
from django.http import HttpResponse


def google_login_token(requests):
    # (Receive token by HTTPS POST)
    token = requests.POST['token']
    try:
        idinfo = client.verify_id_token(token, settings.GOOGLE_CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
        userid = idinfo['sub']
        print idinfo

    except crypt.AppIdentityError:
        print "failed to validated {}".format(token)
        # Invalid token

    return HttpResponse("ok")
