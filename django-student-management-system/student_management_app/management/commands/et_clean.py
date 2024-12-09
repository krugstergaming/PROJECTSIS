from django.core.management.base import BaseCommand
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.db import transaction


class Command(BaseCommand):
    help = "Clean up expired JWT tokens and expired session keys"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # Clean expired tokens
            expired_tokens = OutstandingToken.objects.filter(expires_at__lt=now())
            tokens_deleted = 0

            for token in expired_tokens:
                # Check if the token is blacklisted and delete it
                if hasattr(token, "blacklistedtoken"):
                    token.blacklistedtoken.delete()
                # Delete the outstanding token
                token.delete()
                tokens_deleted += 1

            # Clean blacklisted tokens separately (if not already expired)
            blacklisted_tokens = BlacklistedToken.objects.all()
            blacklisted_deleted = 0

            for blacklisted in blacklisted_tokens:
                token = blacklisted.token
                if token.expires_at >= now():  # Only delete unexpired blacklisted tokens
                    blacklisted.delete()
                    token.delete()
                    blacklisted_deleted += 1

            # Clean expired sessions
            expired_sessions = Session.objects.filter(expire_date__lt=now())
            sessions_deleted = expired_sessions.delete()[0]

            # Output summary
            self.stdout.write(
                f"Deleted {tokens_deleted} expired tokens, "
                f"{blacklisted_deleted} blacklisted tokens, and "
                f"{sessions_deleted} expired sessions."
            )