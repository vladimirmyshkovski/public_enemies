from django import forms
from .models import Enemy
from fluent_comments.forms import CompactLabelsCommentForm
from draceditor.fields import DraceditorFormField

class EnemyForm(forms.ModelForm):
    class Meta:
        model = Enemy
        fields = '__all__'

class VoteForm(forms.ModelForm):
	vote = forms.IntegerField()
	class Meta:
		model = Enemy
		fields = '__all__'