from django import forms

from apps.Nodes.models import Node, Port

class NodeForm(forms.ModelForm):
	
	class Meta:
		model = Node
		fields = [
			'id',
			'name',
		]
		labels = {
			'id': 'Id',
			'name':'Name'
		}
		widgets = {
			'id': forms.TextInput(attrs={'class':'form-control'}),
			'name': forms.TextInput(attrs={'class':'form-control'}),
		}

class PortForm(forms.ModelForm):
	
	class Meta:
		model = Port
		fields = [
			'id',
			'node',
		]
		labels = {
			'id': 'Id',
			'node':'Node'
		}
		widgets = {
			'id': forms.TextInput(attrs={'class':'form-control'}),
			'node': forms.Select(attrs={'class':'form-control'}),
		}

class PortNodeForm(forms.ModelForm):
	
	class Meta:
		model = Port
		fields = [
			'node',
		]
		labels = {
			'node':'Node'
		}
		widgets = {
			'node': forms.Select(attrs={'class':'form-control'}),
		}