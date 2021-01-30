from rest_framework.serializers import ModelSerializer

from apps.Links.models import Link

class LinkSerializer(ModelSerializer):

	class Meta:
		model = Link
		fields = ('id', 'source', 'dest')