"""Fridge model
The ORM’s job is to model the database, but there’s a second system that’s
in charge of actually building the database called migrations.
Its job is to give you the ability to add and remove tables and columns,
based on changes you make to your models.py files.

A new field requires a new migration.
"""

from django.db import models


# Create your models here.
class Item(models.Model):
    # define text field of db needs default
    text = models.TextField(default='')
