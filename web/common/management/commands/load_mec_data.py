from django.core.management.base import BaseCommand, CommandError
from common.models import Item

class Command(BaseCommand):
	help = 'Load MEC item data'

	def add_arguments(self, parser):
		parser.add_argument('quantity', nargs='+', type=int)

	def handle(self, *args, **options):
		for quantity in options['quantity']:
			Item.objects.load_mec_items(quantity)
