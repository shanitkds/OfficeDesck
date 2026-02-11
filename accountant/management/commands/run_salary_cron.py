from django.core.management.base import BaseCommand
from accountant.services import salary_payment_automation


class Command(BaseCommand):
    help = "Run monthly salary automation"

    def handle(self, *args, **kwargs):
        salary_payment_automation()
        self.stdout.write(
            self.style.SUCCESS("Monthly salary automation completed")
        )