from rest_framework.serializers import ModelSerializer

from apps.Nodes.models import Node, Port

class NodeSerializer(ModelSerializer):

	class Meta:
		model = Node
		fields = ('id', 'name')
		
class PortSerializer(ModelSerializer):

	class Meta:
		model = Port
		fields = ('id', 'node')