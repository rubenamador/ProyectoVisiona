from django.db import models

# Create your models here.
from apps.Nodes.models import Node, Port

class Link(models.Model):
	id = models.CharField(max_length=25, primary_key=True)
	source = models.OneToOneField(Port, related_name='source-tp+', null=True, blank=True, on_delete=models.CASCADE)
	dest = models.OneToOneField(Port, related_name='dest-tp+', null=True, blank=True, on_delete=models.CASCADE)
	source_node = models.ForeignKey(Node, related_name='source-node+', null=True, blank=True, on_delete=models.CASCADE)
	dest_node = models.ForeignKey(Node, related_name='dest-node+', null=True, blank=True, on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['id']
	
	def __str__(self):
		return '{}'.format(self.id)
