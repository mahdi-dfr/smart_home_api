from django.core.management import BaseCommand

from project.models import BoardType, NodeType


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(0, 5):
            BoardType.objects.create(name=i)

        for i in range(0, 8):
            NodeType.objects.create(name=i)

        print('added!!')
