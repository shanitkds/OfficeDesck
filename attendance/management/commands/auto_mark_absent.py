from django.core.management.base import BaseCommand
from attendance.services import auto_absent_mark



class Command(BaseCommand):
    help = "Auto mark absent after cutoff"

    def handle(self, *args, **kwargs):
        auto_absent_mark()
        self.stdout.write(self.style.SUCCESS("Auto absent done"))