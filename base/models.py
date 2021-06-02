from django.db import models
from django.contrib.auth.models import User as DUser


class Token(models.Model):
    User = models.OneToOneField(DUser, on_delete=models.CASCADE)
    UUID = models.UUIDField('Token', unique=True)


class Graph(models.Model):
    Title = models.CharField('Title', max_length=150)
    User = models.ForeignKey(DUser, on_delete=models.CASCADE)
    ReadableUser = models.ManyToManyField(DUser, related_name='ReadableUser')

    def __str__(self):
        return f'{self.User.username}: {self.Title}'


class Node(models.Model):
    Title = models.CharField('Title', max_length=150)
    Graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    IsBase = models.BooleanField('IsBase', default=False)

    def __str__(self):
        return self.Title


class Content(models.Model):
    Node = models.ForeignKey(Node, on_delete=models.CASCADE, blank=True, null=True)
    Text = models.TextField('Text', blank=True, null=True)
    Data = models.FileField('Data', blank=True, null=True)
    Ord = models.IntegerField('Ord', default=0)

    def __str__(self):
        return f'{self.Node.Title}: {self.Ord}' if self.Node else 'Empty name'


class Link(models.Model):
    StartNode = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='StartNode')
    EndNode = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='EndNode')
    Weight = models.IntegerField('Weight', default=0)

    def __str__(self):
        return f'{self.StartNode} -> {self.EndNode}: {str(self.Weight)}'

