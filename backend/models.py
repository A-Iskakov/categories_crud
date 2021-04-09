"""
Django ORM Category models for the projects needs
"""

from django.db import models


class UpperCategory(models.Model):
    """
    an upper level category i.e. Phones, TVs, Laptops etc.
    """
    name = models.CharField(max_length=60)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class InnerCategory(models.Model):
    """
    an inner level category i.e. Apple Phones, LED TVs, AMD Laptops etc.
    """
    name = models.CharField(max_length=60)
    upper_category = models.ForeignKey(UpperCategory, on_delete=models.CASCADE, related_name='inner_categories')

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name
