from django.db import models
import uuid

class Invitation(models.Model):
    sender_name = models.CharField(max_length=100, db_column="WYDM_YName")
    recipient_name = models.CharField(max_length=100, db_column="WYDM_DName")
    slug = models.SlugField(unique=True, default=uuid.uuid4, db_column="WYDM_PathName", primary_key=True)
    option = models.IntegerField(db_column="WYDM_OptionTaken")
    message = models.TextField(db_column="WYDM_Message", default="")

    class Meta:
        db_table = "WYDM_T1"