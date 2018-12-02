from django.db import models

from selectize.models import Selectize
from selectize.strategies.render import DjangoTemplateStrategy
from selectize.strategies.search import SearchFieldsStrategy


@Selectize(
    DjangoTemplateStrategy("question"),
    SearchFieldsStrategy(["text"])
)
class Question(models.Model):
    text = models.CharField(
        max_length=200
    )
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True
    )


@Selectize(
    DjangoTemplateStrategy("choice"),
    SearchFieldsStrategy(["text", "question__text"])
)
class Choice(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    text = models.CharField(
        max_length=200
    )
    votes = models.IntegerField(
        default=0
    )
