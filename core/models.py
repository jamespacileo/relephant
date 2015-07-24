from django.db import models
from swampdragon.models import SelfPublishModel
from core.serializers import GameCommentSerializer


# class TodoList(SelfPublishModel, models.Model):
#     serializer_class = TodoListSerializer
#     name = models.CharField(max_length=100)
#     description = models.TextField()


# class TodoItem(SelfPublishModel, models.Model):
#     serializer_class = TodoItemSerializer
#     todo_list = models.ForeignKey(TodoList)
#     done = models.BooleanField(default=False)
#     text = models.CharField(max_length=100)

COMMAND_CHOICES = (
    ("up", "up"),
    ("down", "down"),
    ("left", "left"),
    ("right", "right"),
    ("a", "a"),
    ("b", "b"),
)

class GameComment(SelfPublishModel, models.Model):
    serializer_class = GameCommentSerializer

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    command = models.CharField(db_index=True, max_length=100, null=True, blank=True, choices=COMMAND_CHOICES)

    def __unicode__(self):
        return "%s" %self.comment

    def __str__(self):
        return "%s" %self.comment