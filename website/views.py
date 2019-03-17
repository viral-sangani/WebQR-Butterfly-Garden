from django.shortcuts import render
from .models import user_data
import qrcode
import time
import random
import string
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
	if(request.method == 'POST'):
		if(request.POST['submit']):
			obj = user_data()
			obj.customer_name = request.POST['name']
			obj.customer_email = request.POST['email']
			obj.customer_no = request.POST['no']
			obj.adult = request.POST['adult']
			obj.children = request.POST['children']
			obj.total_price = int(request.POST['adult'])*500+int(request.POST['children'])*350
			obj.qr_link = 'https://qrcode.online/img/?type=text&size=7&data=Name: '+request.POST['name']+' | Number: '+request.POST['no']+' | Adult: '+request.POST['adult']+'| Children: '+request.POST['children']+' |Time: '+time.asctime( time.localtime(time.time()) )
			obj.save()
			img = qrcode.make('Name: '+request.POST['name']+'\nEmail: '+request.POST['email']+'\nNumber: '+request.POST['no']+'\nAdult: '+request.POST['adult']+'\nChildren: '+request.POST['children']+'\nTime: '+time.asctime( time.localtime(time.time()) ))
			with open('qrcodes/'+id_generator()+'.png', 'wb') as f:
				img.save(f)

	return render(request,'website/index.html')


@login_required(login_url="/")
def settings(request):
	return render(request,'website/settings.html')
