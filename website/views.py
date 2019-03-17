from django.shortcuts import render
from .models import user_data, price_table, email_info
import qrcode
import time
import random
import string
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .make_pdf import pdf
import time
import os
import smtplib

def admin_login(request):
	context = []
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if request.GET.get('next', None):
					return HttpResponseRedirect(request.GET['next'])
				return HttpResponseRedirect('/home')

		else:
			content = {
			'error': "Provide Valid Credentials !!"
			}
			return render(request, "registration/login.html",content)

	return render(request,'registration/login.html')

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

@login_required(login_url="/")
def dashboard(request):
	user_data_obj = user_data.objects.all().order_by("time")
	page = request.GET.get('page', 1)
	paginator = Paginator(user_data_obj, 25)

	try:
		user_data_page = paginator.page(page)
	except PageNotAnInteger:
		user_data_page = paginator.page(1)
	except EmptyPage:
		user_data_page = paginator.page(paginator.num_pages)

	context = {
	'user_data_page':user_data_page,
	}
	return render(request,'website/dashboard.html',context)


@login_required(login_url="/")
def home(request):
	price_obj = price_table.objects.filter(pk=1)
	for o in price_obj:
		adult_price = o.adult_price
		children_price = o.children_price

	email_obj = email_info.objects.filter(pk=1)
	for o1 in email_obj:
		email = o1.email
		password = o1.password
		default = o1.default_text

	if(request.method == 'POST'):
		obj = user_data()
		obj.customer_name = request.POST['name']
		obj.customer_email = request.POST['email']
		obj.customer_no = request.POST['no']
		obj.adult = request.POST['adult']
		obj.children = request.POST['children']
		obj.total_price = int(request.POST['adult'])*adult_price+int(request.POST['children'])*children_price
		qr_link = ('https://qrcode.online/img/?type=text&size=7&data=Name: '+request.POST['name']+' | Number: '+request.POST['no']+' | Adult: '+request.POST['adult']+'| Children: '+request.POST['children']+' |Time: '+time.asctime( time.localtime(time.time()))).replace(" ","%20")
		obj.qr_link = qr_link
		obj.save()
		img = qrcode.make('Name: '+request.POST['name']+'\nEmail: '+request.POST['email']+'\nNumber: '+request.POST['no']+'\nAdult: '+request.POST['adult']+'\nChildren: '+request.POST['children']+'\nTime: '+time.asctime( time.localtime(time.time()) ))
		with open('qrcodes/qrcode.png', 'wb') as f:
			img.save(f)
		pdf(request.POST['name'], request.POST['adult'], request.POST['children'], int(request.POST['adult'])*500+int(request.POST['children'])*350, time.asctime( time.localtime(time.time()) ))

		username=email
		password=password
		target=request.POST['email']
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(username, password)
		msg = "Hello Mr/Mrs. "+request.POST['name']+default+qr_link
		server.sendmail(username, target, msg)
		print("Mail send")

	context = {
	'adult_price':adult_price,
	'children_price':children_price,
	}
	return render(request,'website/index.html', context)


@login_required(login_url="/")
def settings(request):
	if(request.method == 'POST'):
		if 'price' in request.POST:
			obj = price_table.objects.filter(pk=1).update(adult_price=request.POST['adult'], children_price = request.POST['children'])
		elif 'email' in request.POST:
			obj = email_info.objects.filter(pk=1).update(email=request.POST['email_id'], password = request.POST['password'],default_text = request.POST['default'])

	obj = price_table.objects.filter(pk=1)
	for o in obj:
		adult_price = o.adult_price
		children_price = o.children_price

	obj1 = email_info.objects.filter(pk=1)

	for o1 in obj1:
		email = o1.email
		password = o1.password
		default_text = o1.default_text
		print()

	context = {
	'adult_price':adult_price,
	'children_price':children_price,
	'default_text':default_text,
	'email':email,
	'password':password,
	}
	return render(request,'website/settings.html', context)

def make_pdf(request):
	return None
