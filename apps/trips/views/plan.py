from apps.trips.models import Plan
from django.shortcuts import render_to_response, redirect
from apps.common.decorators import login_required


@login_required
def create(request):
    plan = Plan.objects.create(name="Unnamed Plan")
    return redirect('edit-trip-plan', plan.pub_id)


@login_required
def list(request):
    context = {"plans": Plan.objects.all()}
    return render_to_response("trips/plan/list.html", context)


@login_required
def edit(request, pub_id):
    context = {"plan": Plan.objects.get(pub_id=pub_id)}
    return render_to_response("trips/plan/edit.html", context)
