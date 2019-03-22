from django.contrib import admin
from .models import user_data,price_table, email_info,daily_counter
# Register your models here.
admin.site.register(user_data)
admin.site.register(price_table)
admin.site.register(email_info)
admin.site.register(daily_counter)