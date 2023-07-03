import uuid
from django.db import models

class BaseModel(models.Model):
    """
    Abstract base model class. To apply in all models.

    Attributes:
        id (UUIDField): Primary key field with a unique identifier.
        created_at (DateTimeField): Field representing the creation timestamp.
        updated_at (DateTimeField): Field representing the last update timestamp.

    Meta:
        abstract (bool): Specifies that this is an abstract base model.
    """

    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
