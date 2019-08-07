import graphene
from apps.trips.models import Plan
from utils.auth import get_authenticated_user


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
    pub_id = graphene.String()

    def mutate(self, info, pub_id, name, summary, route_pub_id, packing_list_pub_id, start_datetime, end_datetime):
        args = (info, pub_id, name, summary, route_pub_id, packing_list_pub_id, start_datetime, end_datetime)
        print(args)
        if pub_id != "null":
            qs = Plan.objects.filter(pub_id=pub_id)
            if not qs.exists():
                return self._mutate_update(*args)
        return CreateOrUpdateTripPlan._mutate_create(self, *args)

    def _mutate_create(self, info, pub_id, name, summary, route_pub_id, packing_list_pub_id, start_datetime, end_datetime):
        print("creating new trip plan")
        user = get_authenticated_user(info)
        if user is None:
            return CreateOrUpdateTripPlan(ok=False)

        import datetime
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
        print("updating new trip plan")
        user = get_authenticated_user(info)
        if user is None:
            return CreateOrUpdateTripPlan(ok=False)

        qs = Plan.objects.filter(pub_id=pub_id)
        if not qs.exists():
            return CreateOrUpdateTripPlan(ok=False)

        if user.pub_id != Plan.user_pub_id:
            return CreateOrUpdateTripPlan(ok=False)

        plan = Plan.objects.create(
            user_pub_id=user.pub_id,
            name=name,
            summary=summary,
            route_pub_id=route_pub_id,
            packing_list_pub_id=packing_list_pub_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        return CreateOrUpdateTripPlan(ok=True, pub_id=plan.pub_id)