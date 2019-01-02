from datetime import datetime

from apps.accounts.models import User
from apps.packing.models import PackingList, PackingListItem
from apps.trips.models import Plan
from apps.routes.models import Route
from apps.common.decorators import login_required

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.middleware.csrf import get_token
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.conf import settings


@login_required
def create(request):
    pub_id = request.GET.get("route")
    if pub_id:
        get_object_or_404(Route, pub_id=pub_id)

    plan = Plan.objects.create(
        name="Unnamed Plan",
        user_pub_id=request.user.pub_id,
        route_pub_id=pub_id,
    )
    return redirect('edit-trip-plan', plan.pub_id)


@login_required
def list(request):
    context = {"plans": request.user.plans}
    return render_to_response("trips/plan/list.html", context)


@login_required
def edit(request, pub_id):
    plan = get_object_or_404(Plan, pub_id=pub_id)
    if request.user.pub_id not in [u.pub_id for u in plan.attendees]:
        return HttpResponseForbidden()

    if request.method == "POST":
        def _str_to_dt(s):
            return datetime.strptime(s, '%Y/%m/%d')

        start = request.POST.get("start")
        if start is not None:
            plan.start_datetime = _str_to_dt(start)

        end = request.POST.get("end")
        if end is not None:
            plan.end_datetime = _str_to_dt(end)

        invite_user_email = request.POST.get("invite_user_email")
        if invite_user_email is not None:
            user, created = User.objects.get_or_create(email=invite_user_email)
            plan.add_attendee(inviting_user=request.user, user=user)

        remove_user_pub_id = request.POST.get("remove_user_pub_id")
        if remove_user_pub_id is not None:
            user = User.objects.get(pub_id=remove_user_pub_id)
            plan.remove_attendee(user)

        plan.save()
        return HttpResponse()

    context = {
        "csrf_token": get_token(request),
        "plan": plan,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    }
    return render_to_response("trips/plan/edit.html", context)


@login_required
def forecast(request, pub_id):
    plan = get_object_or_404(Plan, pub_id=pub_id)
    return JsonResponse(plan.forecast, safe=False)


@login_required
def remove(request, pub_id):
    plan = get_object_or_404(Plan, pub_id=pub_id)
    packing_list = PackingList.objects.filter(pub_id=plan.packing_list_pub_id)
    packing_items = PackingListItem.objects.filter(packing_list_pub_id=plan.packing_list_pub_id)

    packing_items.delete()
    packing_list.delete()
    plan.delete()

    return redirect('list-trip-plans')
