from faker import Faker
from django.core.management.base import BaseCommand
from teacher.models import Class


class Command(BaseCommand):
    help = 'Adds specified in argument number of fake records do Class class'

    def handle(self, *args, **options):
        fake = Faker('pl_PL')
        n = options.get("number", 10)

        for _ in range(int(n)):
            created_at = fake.date_time()
            new_class = Class.objects.create(
                name=fake.bothify(text='#?', letters='ABCDEFG'),
                description=fake.text(80),
                is_active=fake.boolean(),
                created_at=created_at,
                modified_at=created_at + fake.time_delta(5),
            )

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number',
                            type=int, default=10, dest="number",
                            help="Amount of new fake records")

