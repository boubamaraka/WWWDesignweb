# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import uri_to_iri, iri_to_uri

from dowwws.models import *
from dowwws.forms import QuestionForm, ReplyForm


OUR_EMAIL = "sittingmat@email.com"

def index(request):
	print("JOU")
	context = RequestContext(request)
	return render_to_response('index.html', context)

def product(request):
	print("Product")
	context = RequestContext(request)
	return render_to_response('product.html', context)

def buy(request):
	print("Buy")
	context = RequestContext(request)
	querySet = OrderCount.objects.all()
	querySet = querySet.filter(productName = "Sitting Mat");
	if len(querySet) == 0:
		newOrderCount = OrderCount(productName = "Sitting Mat", count = 1)
		newOrderCount.save()
	else:
		orderCount = querySet[0]
		prevCount = orderCount.count
		orderCount.count = prevCount + 1
		orderCount.save()
	return render_to_response('product.html', context)

def contact(request):
	print("contact")
	context = RequestContext(request)
	context['publishedQuestions'] = Question.objects.all().filter(isPublished=True)
	context['form'] = QuestionForm()
	#print(context)
	return render_to_response('contact.html', context)

def moderate(request):
	print("moderate")
	context = RequestContext(request)
	if request.user.is_authenticated():
		print("User is authenticated")
		context['approvedQuestions'] = Question.objects.all().filter(isAnswered=False)
		context['form'] = ReplyForm()
		#print(context)
		return render_to_response('moderate.html', context)
	else:
		print("User is not authenticated")
		return render_to_response('login.html', context)

def loginUser(request):
	context = RequestContext(request)
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		print("User is not None")
		if user.is_active:
			print("User is active")
			login(request, user)
			return HttpResponseRedirect('/moderate/')
		else:
			print("User is not active")
			return render_to_response('login.html', context)
	else:
		return render_to_response('login.html', context)

def registerUser(request):
	context = RequestContext(request)
	username = request.POST['username']
	password = request.POST['password']
	user = User.objects.create_user(username, password = password)
	user.save()
	return render_to_response('login.html', context)

def logOutUser(request):
	context = RequestContext(request)
	logout(request)
	return render_to_response('login.html', context)



def travelguide(request):
	print("travelguide")
	context = RequestContext(request)
	return render_to_response('travelguide.html', context)

def newQuestion(request):
	print("newQuestion")
	if request.method == 'POST':
		context = RequestContext(request)
		print(request.POST)
		form = QuestionForm(request.POST or None)
		print(form)

		if form.is_valid():
			print(form.cleaned_data)
			firstName = form.cleaned_data["name"]
			#telNum = form.cleaned_data.get("name")
			email = form.cleaned_data.get("email")
			question = form.cleaned_data.get("message")
			public = form.cleaned_data.get("public")
			emailResponse = form.cleaned_data.get("emailResponse")
			# newQuestion = form.save(commit=False)
			# print(request)
			newQuestion = Question()
			# for var in request:
			# 	print(var)
			# serializedStr = uri_to_iri(request.POST.get('serialized'))
			# print(serializedStr)
			# print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			# print(uri_to_iri(serializedStr))
			# arr = serializedStr.split("&")
			# firstName = arr[1].split("=")[1].replace("+", " ")
			# telNum = arr[2].split("=")[1].replace("+", " ")
			# email = arr[3].split("=")[1].replace("+", " ")
			# title = arr[4].split("=")[1].replace("+", " ").replace("%40", "@").replace("%3F", "?").replace("%E2%82%AC", "€")
			# question = arr[4].split("=")[1].replace("+", " ")

			# public = None
			# emailResponse = None

			# if len(arr) > 5:
			# 	checkboxValue = arr[5].split("=")[1].replace("+", " ")
			# 	if arr[5].split("=")[0] == "public":
			# 		public = "on"
			# 		print("Public ON")
			# 	else:
			# 		print(arr[5].split("=")[0])
			# 		print("EmailResponse ON")
			# 		emailResponse = "on"
			# if len(arr) > 6:
			# 	emailResponse = arr[6].split("=")[1].replace("+", " ")

			newQuestion.name = firstName #request.POST.get('name')
			print(firstName)
			newQuestion.email = email #request.POST.get('email')
			print(email)
			newQuestion.message = question #request.POST.get('message')
			print(question)
			#newQuestion.title = title #request.POST.get('message')
			newQuestion.public = public
			print(public)
			newQuestion.emailResponse = emailResponse
			print(emailResponse)
			# print(public)
			# print(public == None)
			# if public == None:
			# 	newQuestion.public = False
			# 	print("public = False")

			# print(emailResponse)
			# print(emailResponse != None)
			# print(emailResponse == "on")
			# if emailResponse != None and emailResponse == "on":
			# 	newQuestion.emailResponse = True
			# 	print("emailResponse = True")
			newQuestion.save()
			return contact(request)
		else:
			print("FORM NOT VALID")
			print(form)
			print(request.POST.get('serialized'))

def newReply(request):
	print("newReply")
	if request.method == 'POST':
		context = RequestContext(request)
		print(request)
		form = ReplyForm(request.POST or None)
		print(form)
		print("!!!!!!!!!!!!!")
		for var in request:
			print(var)
		print("!!!!!!!!!!!!")

		if form.is_valid():
			print(form.cleaned_data)

			serializedStr = uri_to_iri(request.POST)
			print(serializedStr)
			arr = serializedStr.split("&")
			#arr = json.loads(serializedStr)
			print("ARR")
			for var in arr:
				print(var)
			print("END")
			#postMessage = arr[0].split("=")[1].replace("+", " ")
			#postMessage = arr[0][0]
			#postMessage = arr.get("message")
			postMessage = request.POST.get("message")
			print(postMessage)
			#postId = arr[1].split("=")[1].replace("+", " ")
			postId = request.POST.get("id")
			print(postId)
			postTitle = form.cleaned_data.get("title")
			#postTitle = arr[2].split("=")[1].replace("+", " ")
			print(postTitle)
			postAnswer = form.cleaned_data.get("answer")
			#postAnswer = arr[3].split("=")[1].replace("+", " ")
			print(postAnswer)

			public = request.POST.get("public")
			emailResponse = request.POST.get("emailResponse")

			# last = arr[len(arr)-1]
			# secToLast = arr[len(arr)-2]

			# if last.split("=")[0] == "emailResponse":
			# 	emailResponse = last.split("=")[1].replace("+", " ")
			# 	if secToLast.split("=")[0] == "public":
			# 		public = secToLast.split("=")[1].replace("+", " ")

			# if last.split("=")[0] == "public":
			# 	public = last.split("=")[1].replace("+", " ")

			print(public)
			print(emailResponse)

			# if len(arr) > 4:
			# 	checkboxValue = arr[4].split("=")[1].replace("+", " ")
			# 	if arr[4].split("=")[0] == "public":
			# 		public = "on"
			# 	else: 
			# 		emailResponse = "on"
			# 	print(public)

			# if len(arr) > 5:
			# 	emailResponse = arr[5].split("=")[1].replace("+", " ")
			# 	print(emailResponse)

			querySet = Question.objects.all()
			querySet = querySet.filter(id = int(postId))
			question = querySet[0]
			print(len(querySet))
			#print(str(question))
			#postAnswer = request.POST.get('answer')
			question.answer = postAnswer
			question.title = postTitle
			question.isAnswered = True
			if public != None and public == "on":
				question.isPublished = True

			if emailResponse != None and emailResponse == "on":
				print("send Mail")
				send_mail('Subject here', 'Here is the message.', OUR_EMAIL,
	    [question.email], fail_silently=False)


				#send_mail('Subject here', 'Here is the message.', 'from@example.com',
	    #['to@example.com'], fail_silently=False)

			question.save()
			return moderate(request)

		else:
			print("FORM NOT VALID")
			print(form)
			print(request.POST.get('serialized'))

