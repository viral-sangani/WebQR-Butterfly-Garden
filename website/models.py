from django.db import models

class user_data(models.Model):
    customer_name = models.CharField(max_length=200, default='')
    customer_email = models.EmailField(max_length=200, blank=False)
    customer_no = models.IntegerField()
    adult = models.IntegerField()
    children = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    # date.editable=True
    time = models.TimeField(auto_now_add=True)
    # time.editable=True
    qr_link = models.CharField(max_length=2000, default='')
    # total_price = models.IntegerRangeField(max_value = 100000)

    def __str__(self):
        return self.customer_name + " - " + self.customer_email

# class price_table(models.Model):
#     adult_price = models.IntegerField()


    def __str__(self):
        return self.customer_name + " - " + self.customer_email
