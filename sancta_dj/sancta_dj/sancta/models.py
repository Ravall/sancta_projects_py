from django.db import models

# Create your models here.
class MfSystemArticle(models.Model):
    class Meta:
        db_table = u'mf_system_article'
        managed = False
        app_label = 'sancta'