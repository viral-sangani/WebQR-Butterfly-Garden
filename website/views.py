from django.shortcuts import render
from .models import user_data
import qrcode
import time
import random
import string
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect

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



def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def dashboard(request):
	user_data_obj = user_data.objects.all().order_by("time")
	context = {
	'user_data_obj':user_data_obj,
	}
	return render(request,'website/dashboard.html',context)

def home(request):
	if(request.method == 'POST'):
		if(request.POST['submit']):
			obj = user_data()
			obj.customer_name = request.POST['name']
			obj.customer_email = request.POST['email']
			obj.customer_no = request.POST['no']
			obj.adult = request.POST['adult']
			obj.children = request.POST['children']
			# obj.total_price = request.POST['adult']*500+request.POST['children']*350
			obj.qr_link = 'https://qrcode.online/img/?type=text&size=7&data=Name: '+request.POST['name']+' | Number: '+request.POST['no']+' | Adult: '+request.POST['adult']+'| Children: '+request.POST['children']+' |Time: '+time.asctime( time.localtime(time.time()) )
			obj.save()
			img = qrcode.make('Name: '+request.POST['name']+'\nEmail: '+request.POST['email']+'\nNumber: '+request.POST['no']+'\nAdult: '+request.POST['adult']+'\nChildren: '+request.POST['children']+'\nTime: '+time.asctime( time.localtime(time.time()) ))
			with open('qrcodes/'+id_generator()+'.png', 'wb') as f:
				img.save(f)

	return render(request,'website/index.html')

def settings(request):

	return render(request,'website/settings.html')
