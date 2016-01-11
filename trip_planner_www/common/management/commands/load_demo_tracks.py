from django.core.management.base import BaseCommand, CommandError
from common.models import Route

class Command(BaseCommand):
	help = 'Load demo tracks'

	def handle(self, *args, **options):
		Route.objects.load_demo_tracks()
