from datetime import datetime

from apps.trips.models import Plan
from apps.routes.models import Route
from apps.common.decorators import login_required

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.conf import settings


@login_required
def create(request):
    route = None
    pub_id = request.GET.get("route")
    if pub_id:
        route = get_object_or_404(Route, pub_id=pub_id)

    plan = Plan.objects.create(name="Unnamed Plan", route_pub_id=route.pub_id)
    return redirect('edit-trip-plan', plan.pub_id)


@login_required
def list(request):
    context = {"plans": Plan.objects.all()}
    return render_to_response("trips/plan/list.html", context)


@login_required
def edit(request, pub_id):
    plan = get_object_or_404(Plan, pub_id=pub_id)

    if request.method == "POST":
        def _str_to_dt(s):
            return datetime.strptime(s, '%Y/%m/%d')

        start = request.POST.get("start")
        if start is not None:
            plan.start_datetime = _str_to_dt(start)

        end = request.POST.get("end")
        if end is not None:
            plan.end_datetime = _str_to_dt(end)

        plan.save()
        return HttpResponse()

    context = {
        "csrf_token": get_token(request),
        "plan": plan,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    }
    return render_to_response("trips/plan/edit.html", context)
