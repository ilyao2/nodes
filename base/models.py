from django.db import models
from django.contrib.auth.models import User as DUser

# TODO: Придумать, как обозначить базовый узел


class Graph(models.Model):
    Title = models.CharField('Title', max_length=150)
    User = models.ForeignKey(DUser, on_delete=models.CASCADE)
    ReadableUser = models.ManyToManyField(DUser, related_name='ReadableUser')

    def __str__(self):
        return f'{self.User.username}: {self.Title}'


class Content(models.Model):
    Title = models.CharField('Title', max_length=150)
    Text = models.TextField('Text')
    Data = models.FileField('Data', blank=True, null=True)
    Ord = models.IntegerField('Ord', blank=True, null=True, default=None)

    def __str__(self):
        return self.Title


class Node(models.Model):
    Graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    Content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Content.Title


class Link(models.Model):
    StartNode = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='StartNode')
    EndNode = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='EndNode')
    Weight = models.IntegerField('Вес', default=0)

    def __str__(self):
        return self.Weight

