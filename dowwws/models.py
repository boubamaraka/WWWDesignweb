from django.db import models

class Question(models.Model):
	name = models.CharField(null=False,blank=False, max_length=255) # The name of the client
	title = models.CharField(null=False,blank=False, max_length=255, default="No Title") # The title of the question
	email = models.CharField(null=False,blank=False, max_length=255) # The name of the client
	message = models.TextField(null=False, blank=False) # The Question
	answer = models.TextField(null=False, blank=False, default="Not answered yet") # The Question
	postDate = models.DateField(auto_now=False, auto_now_add=True) # When the question was asked
	isPublished = models.BooleanField(default=False) # Has admin published the question
	isAnswered = models.BooleanField(default=False) # Has admin answered the question
	public = models.BooleanField(default=True) # Will the answer be published
	emailResponse = models.BooleanField(default=False) # Will the answer be send to the client with email

	def __str__(self):
		return str(self.name) + "\n" + str(self.message) + "\n" + str(self.answer)

class OrderCount(models.Model):
	productName = models.CharField(null=False,blank=False, max_length=255) # The name of the product
	count = models.IntegerField(default=0) # How many orders there are