import time
import sendwithus as swu

INVITATION_EMAIL_SWU_ID = "tem_JGCSJtVfB8HkMjT9T3JgbqjC"


def _send(email_id, email_data, recipient):
    while True:
        resp = swu.api.send(
            email_id=email_id,
            email_data=email_data,
            recipient=recipient,
            sender="noreply@triptracks.io",
        )
        if resp.status_code == 200:
            break
        print resp.content
        time.sleep(10)


def send_trip_invitation_email(from_user, to_user, trip):
    data = {
        "trip": {
            "location": trip.name,
            "start_datetime": trip.start_datetime,
            "end_datetime": trip.end_datetime,
        },
        "invitor": {
            "name": from_user.email,
        },
        "invitation_url": "https://apps.triptracks.io/trip/plan/edit/{pub_id}".format(pub_id=trip.pub_id),
    }
    _send(
        email_id=INVITATION_EMAIL_SWU_ID,
        email_data=data,
        recipient=to_user.email,
    )
