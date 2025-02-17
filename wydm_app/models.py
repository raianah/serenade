from django.db import models
import uuid

class Invitation(models.Model):
    sender_name = models.CharField(max_length=100, db_column="your-table-column")
    recipient_name = models.CharField(max_length=100, db_column="your-table-column")
    slug = models.SlugField(unique=True, default=uuid.uuid4, db_column="your-table-column", primary_key=True)
    option = models.IntegerField(db_column="your-table-column")
    message = models.TextField(db_column="your-table-column", default="")

    class Meta:
        db_table = "your-table-name"