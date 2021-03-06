from django.core.management.base import BaseCommand, CommandError

from subscriptions.feeds import import_all_feeds
from subscriptions.feeds import SubscriptionEmailer
from subscriptions.models import Subscriber, User

class Command(BaseCommand):
    help = "Create subscribers for all those users that don't have one."

    def handle(self, *args, **options):
        for user in User.objects.all():
            Subscriber.objects.get_or_create_for_user(user)
