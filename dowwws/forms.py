from django import forms
from dowwws.models import Question

class QuestionForm(forms.Form):
	name = forms.CharField(required = False, max_length=255)
	#title = forms.CharField() # The title of the question
	email = forms.CharField(required = False, max_length=255) # The name of the client
	message = forms.CharField(required = False, widget=forms.Textarea) # The Question
	#answer = forms.CharField() # The Question
	#postDate = forms.DateField() # When the question was asked
	#isPublished = forms.BooleanField() # Has admin published the question
	#isAnswered = forms.BooleanField() # Has admin answered the question
	public = forms.BooleanField(label = "Can the question be shown publicly?", required = False) # Will the answer be published
	emailResponse = forms.BooleanField(label = "Do you want the answer sent also to your email?", required = False) # Will the an
	# class Meta:
	# 	model = Question
	# 	fields = ('name', 'email', 'message')

class ReplyForm(forms.Form):
	#name = forms.CharField(required = False, max_length=255)
	title = forms.CharField(required = False) # The title of the question
	#email = forms.CharField(required = False, max_length=255) # The name of the client
	#message = forms.CharField(required = False, widget=forms.Textarea) # The Question
	answer = forms.CharField(required = False, widget=forms.Textarea) # The Question
	#postDate = forms.DateField() # When the question was asked
	#isPublished = forms.BooleanField() # Has admin published the question
	#isAnswered = forms.BooleanField() # Has admin answered the question
	#public = forms.BooleanField(label = "Can the question be shown publicly?", required = False) # Will the answer be published
	#emailResponse = forms.BooleanField(label = "Do you want the answer sent also to your email?", required = False) # Will the an
	# class Meta:
	# 	model = Question
	# 	fields = ('name', 'email', 'message')

def clean(self):
	cleaned_data = super(QuestionForm, self).clean()
	# do your custom validations / transformations here
	# and some more
	return cleaned_data