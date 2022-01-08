from django.contrib.auth.models import User
from django.db import models


class Workspace(models.Model):
    name = models.CharField(max_length=64)


class Board(models.Model):
    name = models.CharField(max_length=64)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)


class List(models.Model):
    name = models.CharField(max_length=64)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Card(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateTimeField(null=True)
    description = models.CharField(max_length=256)
    list = models.ForeignKey(List, on_delete=models.CASCADE)


class Attachment(models.Model):
    name = models.CharField(max_length=256)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    file = models.FileField(null=True, blank=True, upload_to='/media/')


class Comment(models.Model):
    text = models.CharField(max_length=256)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=True)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # board = models.ManyToManyField(Board, null=True)
    workspace = models.ManyToManyField(Workspace, null=True)
