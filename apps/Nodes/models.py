from django.db import models

# Create your models here.

class Node(models.Model):
	id = models.CharField(max_length=25, primary_key=True)
	name = models.CharField(max_length=25, default='')
	
	class Meta:
		ordering = ['id']
		
	def __str__(self):
		return '{}'.format(self.id)

class Port(models.Model):
	id = models.CharField(max_length=25, primary_key=True)
	node = models.ForeignKey(Node, null=True, blank=True, on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['id']
		
	def __str__(self):
		return '{}'.format(self.id)
