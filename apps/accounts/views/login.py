from django.conf import settings
from oauth2client import client, crypt
from django.http import HttpResponse, HttpResponseForbidden
from apps.accounts.models import User


def google_login_token(requests):
    token = requests.POST.get('token')
    try:
        idinfo = client.verify_id_token(token, settings.GOOGLE_CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
        email = idinfo['email']
        users = User.objects.filter(email=email)

        if len(users) > 1:
            raise Exception("multiple users with email:{}".format(email))

        if len(users) == 0:
            user = User.objects.create(email=email, google_credentials=idinfo)
            print "new user: {} {}".format(email, user.pub_id)

        else:
            user = users[0]

        print "user logged in: {} {}".format(email, user.pub_id)

    except crypt.AppIdentityError:
        print "failed to validated {}".format(token)
        return HttpResponseForbidden("nope")

    return HttpResponse("ok")