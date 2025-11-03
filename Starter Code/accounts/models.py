from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid



class EmailOTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['email', 'code']),
        ]

    def is_expired(self):
        return self.expires_at < timezone.now()
