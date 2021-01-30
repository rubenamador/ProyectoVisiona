from django import forms

from apps.Links.models import Link

class LinkForm(forms.ModelForm):
	
	class Meta:
		model = Link
		fields = [
			'id',
			'source',
			'dest',
		]
		labels = {
			'id': 'Id',
			'source': 'Source',
			'dest': 'Destination',
		}
		widgets = {
			'id': forms.TextInput(attrs={'class':'form-control'}),
			'source': forms.Select(attrs={'class':'form-control'}),
			'dest': forms.Select(attrs={'class':'form-control'}),
		}