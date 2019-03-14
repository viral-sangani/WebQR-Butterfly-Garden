from django.shortcuts import render
from .models import user_data
import qrcode
import time
import random
import string
# Create your views here.

def home(request):
    if(request.method == 'POST'):
        if(request.POST['submit']):
            obj = user_data()
            obj.customer_name = request.POST['name']
            obj.customer_email = request.POST['email']
            obj.customer_no = request.POST['no']
            obj.adult = request.POST['adult']
            obj.children = request.POST['children']
            obj.save()
            img = qrcode.make('Name: '+request.POST['name']+'\nEmail: '+request.POST['email']+'\nNumber: '+request.POST['no']+'\nAdult: '+request.POST['adult']+'\nChildren: '+request.POST['children']+'\nTime: '+time.asctime( time.localtime(time.time()) ))
            with open('qrcodes/'+id_generator()+'.png', 'wb') as f:
                img.save(f)
            print('https://qrcode.online/img/?type=text&size=7&data=Name: '+request.POST['name']+' | Number: '+request.POST['no']+' | Adult: '+request.POST['adult']+'| Children: '+request.POST['children']+' |Time: '+time.asctime( time.localtime(time.time()) ))


    return render(request,'website/index.html')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
