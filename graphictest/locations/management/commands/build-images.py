import datetime
from optparse import make_option
from django.core.management import BaseCommand, CommandError
from locations.helper import LocationsGraph


class Command(BaseCommand):

    help = """Command for images build"""


    def add_arguments(selfself, parser):
        parser.add_argument(
            '--today',
            action='store_true',
            dest='today',
            help='Get data till today'
        )

        parser.add_argument(
            '--date',
            action='store',
            dest='date',
            help='Get data till given date'
        )

        parser.add_argument(
            '--days',
            action='store',
            dest='days',
            help='Get data for given days amount'
        )

    def handle(self, *args, **options):
        if not options['today'] and not options['date']:
            return 'You need to set --today or --date=<dd/mm/yyyy> option for target date'

        if not options['days']:
            return 'You need to set days amount with option --days=<amount>'

        try:
            days_amount = int(options['days'])
        except ValueError:
            return 'Please use number as days amount'

        if options['today']:
            to_date = datetime.datetime.utcnow()

        if options['date']:
            try:
                to_date = datetime.datetime.strptime(options['date'], '%d/%m/%Y')
            except ValueError:
                return 'Please use date in format dd/mm/yyyy'

        from_date = to_date - datetime.timedelta(days=days_amount)
        print('Create graph data from {} to {}'.format(from_date.strftime('%d/%m/%Y'), to_date.strftime('%d/%m/%Y')))

        # Get graphs for given date range
        my_graph = LocationsGraph(from_date=from_date, to_date=to_date)
        my_graph.get_graphs()
