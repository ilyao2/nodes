from django.db import models


class User(models.Model):
    class Meta:
        abstract = True

    loginNSTU = models.CharField('Логин', max_length=200, unique=True, null=True)


class Graph(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.User


class Node(models.Model):
    Graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    Content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def __str__(self):
        return self.Content


class Content(User):
    Text = models.TextField('Text')
    Data = models.FileField('Data')
    Ord = models.IntegerField('Ord')

    def __str__(self):
        return self.Text


class Link(models.Model):
    StartNode = models.ForeignKey(Node, on_delete=models.CASCADE)
    EndNode = models.ForeignKey(Node, on_delete=models.CASCADE)
    Weight = models.IntegerField('Вес')

    def __str__(self):
        return self.Weight

