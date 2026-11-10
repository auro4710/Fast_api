from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True,generated=True)
    name = fields.CharField(unique=True, max_length=100)
    age = fields.IntField()