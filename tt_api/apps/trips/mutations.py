import datetime
import graphene
from apps.trips.models import Plan
from utils.auth import get_authenticated_user


class DeleteTripPlan(graphene.Mutation):
    class Arguments:
        pub_id = graphene.String()

    ok = graphene.Boolean()
    reason = graphene.String()

    def mutate(self, info, pub_id):
        user = get_authenticated_user(info)
        if user is None:
            return DeleteTripPlan(ok=False, reason="unauthed")

        qs = Plan.objects.filter(pub_id=pub_id, user_pub_id=user.pub_id)
        if qs.count() != 1:
            return DeleteTripPlan(ok=False, reason="not owner")

        qs.delete()
        return DeleteTripPlan(ok=True)


class CreateOrUpdateTripPlan(graphene.Mutation):
    class Arguments:
        pub_id = graphene.String()
        name = graphene.String()
        summary = graphene.String()
        route_pub_id = graphene.String()
        packing_list_pub_id = graphene.String()
        start_datetime = graphene.Float()
        end_datetime = graphene.Float()

    ok = graphene.Boolean()
    reason = graphene.String()
    pub_id = graphene.String()

    def mutate(self, info, pub_id, name, summary, route_pub_id, packing_list_pub_id, start_datetime, end_datetime):
        args = (info, pub_id, name, summary, route_pub_id, packing_list_pub_id, start_datetime, end_datetime)
        user = get_authenticated_user(info)
        if user is None:
            return CreateOrUpdateTripPlan(ok=False)

        qs = Plan.objects.filter(pub_id=pub_id, user_pub_id=user.pub_id)
        if qs.exists():
            return CreateOrUpdateTripPlan._mutate_update(self, *args)
        return CreateOrUpdateTripPlan._mutate_create(self, *args)

    def _mutate_create(self, info, pub_id, name, summary, route_pub_id, packing_list_pub_id, start_datetime, end_datetime):
        user = get_authenticated_user(info)
        if user is None:
            return CreateOrUpdateTripPlan(ok=False)

        plan = Plan.objects.create(
            user_pub_id=user.pub_id,
            name=name,
            summary=summary,
            route_pub_id=route_pub_id,
            packing_list_pub_id=packing_list_pub_id,
            start_datetime=datetime.datetime.fromtimestamp(start_datetime),
            end_datetime=datetime.datetime.fromtimestamp(end_datetime),
        )
        return CreateOrUpdateTripPlan(ok=True, pub_id=plan.pub_id)

    def _mutate_update(self, info, pub_id, name, summary, route_pub_id, packing_list_pub_id, start_datetime, end_datetime):
        user = get_authenticated_user(info)
        if user is None:
            return CreateOrUpdateTripPlan(ok=False, reason="unauthenticated")

        qs = Plan.objects.filter(pub_id=pub_id)
        if not qs.exists():
            return CreateOrUpdateTripPlan(ok=False, reason="nonexistant plan")
        plan = qs[0]

        if user.pub_id != plan.user_pub_id:
            return CreateOrUpdateTripPlan(ok=False, reason="invalid ownership")

        Plan.objects.filter(pub_id=pub_id, user_pub_id=user.pub_id).update(
            name=name,
            summary=summary,
            route_pub_id=route_pub_id,
            packing_list_pub_id=packing_list_pub_id,
            start_datetime=datetime.datetime.fromtimestamp(start_datetime),
            end_datetime=datetime.datetime.fromtimestamp(end_datetime),
        )
        return CreateOrUpdateTripPlan(ok=True, pub_id=plan.pub_id, reason="")
