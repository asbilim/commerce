# core/models.py (or wherever you keep common models)
import uuid
from django.db import models

class UUIDModel(models.Model):
    """
    Abstract base model that sets 'id' as a UUID primary key.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True
