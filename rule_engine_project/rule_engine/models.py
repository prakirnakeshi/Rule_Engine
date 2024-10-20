from django.db import models

# Create your models here.
from django.db import models

class Rule(models.Model):
    rule_string = models.TextField()

    def __str__(self):
        return self.rule_string
