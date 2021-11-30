from django.contrib.auth.models import User
from django.db import models


class Workspace(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Board(models.Model):
    name = models.CharField(max_length=200, unique=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)


class List(models.Model):
    name = models.CharField(max_length=200, unique=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Card(models.Model):
    name = models.CharField(max_length=200, unique=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE)


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ManyToManyField(Board)
    workspace = models.ManyToManyField(Workspace)
