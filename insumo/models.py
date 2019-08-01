from django.db import models


class Insumos(models.Model):
    name = models.CharField(max_length=255, null=False)

    machine = models.CharField(max_length=255, null=False)


    def __str__(self):
        return "{} - {}".format(self.name, self.machine)