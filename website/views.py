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
import xlwt

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
	user_data_obj = user_data.objects.all().order_by("pk")
	page = request.GET.get('page', 1)
	paginator = Paginator(user_data_obj, 25)

	try:
		user_data_page = paginator.page(page)
	except PageNotAnInteger:
		user_data_page = paginator.page(1)
	except EmptyPage:
		user_data_page = paginator.page(paginator.num_pages)
	count = user_data.objects.all().count()
	context = {
	'user_data_page':user_data_page,
	'count':count,
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
		if request.POST['name'] == "":
			name_n = "N/a"
		else:
			name_n = request.POST['name']

		current_time = time.asctime( time.localtime(time.time()) )
		formatted_time = current_time[:10]+"--"+current_time[11:13]+"-"+current_time[14:16]+"-"+current_time[17:19]
		formatted_time1 = current_time[:10]+" "+current_time[11:13]+"-"+current_time[14:16]+"-"+current_time[17:19]
		total_price = int(request.POST['adult'])*adult_price+int(request.POST['children'])*children_price
		qr_link = ('https://qrcode.online/img/?type=text&size=7&data=Name- '+	name_n+' | Total- '+str(total_price)+' THB | Number- '+request.POST['no']+' | Adult- '+request.POST['adult']+'| Children- '+request.POST['children']+' |Time- '+formatted_time).replace(" ","%20")


		obj = user_data()
		obj.customer_name = name_n
		print(name_n)
		if request.POST['email'] == "":
			obj.customer_email = "None"
		else:
			obj.customer_email = request.POST['email']

		if request.POST['no'] == "":
			obj.customer_no = "0"
		else:
			obj.customer_no = request.POST['no']

		obj.adult = request.POST['adult']

		if request.POST['children'] == "":
			obj.children = "0"
		else:
			obj.children = request.POST['children']

		obj.total_price = total_price
		obj.qr_link = qr_link
		obj.date_time = formatted_time
		obj.save()

		

		img = qrcode.make('Name- '+name_n+'\nTotal- '+str(total_price)+'\nEmail- '+request.POST['email']+'\nNumber- '+request.POST['no']+'\nAdult- '+request.POST['adult']+'\nChildren- '+request.POST['children']+'\nTime- '+formatted_time1)
		with open('qrcodes/qrcode.png', 'wb') as f:
			img.save(f)
		pdf(name_n, request.POST['adult'], request.POST['children'], str(total_price), time.asctime( time.localtime(time.time()) ))

		if request.POST['email'] != "":
			username=email
			password=password
			target=request.POST['email']
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.login(username, password)
			subject = "QR Ticket Of Butterfly Garden"
			body = default + "\n" + qr_link
			headers = ["From: " + email,
				"Subject: "+ subject,
				"To: "+ name_n,
				"MIME-Version: 1.0",
	               "Content-Type: text/html"]
			headers = "\r\n".join(headers)
			server.sendmail(username, target, headers + "\r\n\r\n" +  body)

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
		elif 'delete' in request.POST:
			obj = user_data.objects.all().delete()
			user_data.objects.create(customer_name="sample", customer_email="N/a",customer_no="0",adult="0",children="0",date_time="0",qr_link="0",total_price="0")

	obj = price_table.objects.filter(pk=1)
	for o in obj:
		adult_price = o.adult_price
		children_price = o.children_price

	obj1 = email_info.objects.filter(pk=1)

	for o1 in obj1:
		email = o1.email
		password = o1.password
		default_text = o1.default_text

	context = {
	'adult_price':adult_price,
	'children_price':children_price,
	'default_text':default_text,
	'email':email,
	'password':password,
	}
	return render(request,'website/settings.html', context)

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="database.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Customer Name', 'Customer Email', 'Customer No', 'Adult', 'Children','Date & Time','Total Price',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = user_data.objects.all().values_list('customer_name', 'customer_email', 'customer_no', 'adult','children','date_time','total_price')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

