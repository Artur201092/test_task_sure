from django.conf import settings
import pandas as pd
from apps.users.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print('Adding Data...')

        """ add DB data """

        # add_Brand_data
        df = pd.read_csv(settings.BASE_DIR + '/fixtures/users.csv')
        if len(df) > User.objects.all().count():
            for index, row in df.iterrows():
                user = User()
                try:
                    user_obj = User.objects.filter(email=row["email"]).first()
                    if not user_obj:
                        user.save()
                except User.DoesNotExist:
                    raise CommandError('User "%s" does not exist' % row["name"])

        print("Data added successfully!!!")