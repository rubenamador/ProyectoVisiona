from django import forms

from apps.Links.models import Link

class LinkForm(forms.ModelForm):
	
	class Meta:
		model = Link
		fields = [
			'id',
			'source',
			'dest',
			'source_node',
			'dest_node',
		]
		labels = {
			'id': 'Id',
			'source': 'Source',
			'dest': 'Destination',
			'source_node': 'Source-Node',
			'dest_node': 'Dest-Node',
		}
		widgets = {
			'id': forms.TextInput(attrs={'class':'form-control'}),
			'source': forms.Select(attrs={'class':'form-control'}),
			'dest': forms.Select(attrs={'class':'form-control'}),
			'source_node': forms.Select(attrs={'class':'form-control'}),
			'dest_node': forms.Select(attrs={'class':'form-control'}),
		}