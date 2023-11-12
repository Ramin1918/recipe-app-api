"""
Django command to wait for the database to be available.
"""
import time
import logging

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Django command to wait for the database to be available.'

    def handle(self, *args, **options):
        self.stdout.write('Waiting for the database...')
        db_up = False
        retries = 0
        max_retries = 30  # Adjust the number of retries as needed

        while not db_up and retries < max_retries:
            try:
                self.check(databases=['default'])
                db_up = True
            except (OperationalError, Psycopg2OpError) as e:
                logger.warning(f'Database unavailable: {e}. Retrying in 1 second...')
                time.sleep(1)
                retries += 1

        if db_up:
            self.stdout.write(self.style.SUCCESS('Database available!'))
        else:
            self.stderr.write(self.style.ERROR('Unable to connect to the database within the specified time.'))
