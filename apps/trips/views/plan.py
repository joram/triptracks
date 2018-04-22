from apps.trips.models import Plan
from django.shortcuts import render_to_response, redirect


def create(request):
    plan = Plan.objects.create(name="Unnamed Plan")
    return redirect('edit-trip-plan', plan.pub_id)


def list(request):
    context = {"plans": Plan.objects.all()}
    return render_to_response("trips/plan/list.html", context)


def edit(request, pub_id):
    context = {"plan": Plan.objects.get(pub_id=pub_id)}
    return render_to_response("trips/plan/edit.html", context)
