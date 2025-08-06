from django.core.management.base import BaseCommand
from notifications.models import PushSubscription
from notifications.utils import send_push_notification
from pywebpush import WebPushException

class Command(BaseCommand):
    help = 'Remove expired or invalid push subscriptions from the database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Checking for expired push subscriptions...'))
        count = 0
        test_payload = {"title": "Test", "body": "Subscription check."}
        for sub in PushSubscription.objects.all():
            try:
                # Try sending a test push (will auto-remove if expired due to utils.py logic)
                send_push_notification(sub, test_payload)
            except WebPushException as ex:
                if hasattr(ex, 'response') and ex.response is not None and ex.response.status_code == 410:
                    count += 1
                    self.stdout.write(self.style.WARNING(f"Removed expired subscription: {sub.endpoint}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Error for {sub.endpoint}: {ex}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Unexpected error for {sub.endpoint}: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Cleanup complete. {count} expired subscriptions removed.")) 