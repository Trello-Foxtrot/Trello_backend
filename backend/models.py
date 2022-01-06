from django.contrib.auth.models import User
from django.db import models


class Workspace(models.Model):
    name = models.CharField(max_length=200)


class Board(models.Model):
    name = models.CharField(max_length=200)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)


class List(models.Model):
    name = models.CharField(max_length=200)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Card(models.Model):
    name = models.CharField(max_length=200)
    list = models.ForeignKey(List, on_delete=models.CASCADE)


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=True)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # board = models.ManyToManyField(Board, null=True)
    workspace = models.ManyToManyField(Workspace, null=True)
