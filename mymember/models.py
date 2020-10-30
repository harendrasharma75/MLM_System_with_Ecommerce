from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class AnonymousQuery(models.Model):
    name = models.CharField(max_length=50)
    phone=models.CharField(max_length=12)
    email=models.EmailField()
    desc = models.TextField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.name



profile_status=(('Active','Active'),('Inactive','Inactive'))
gender_select=(('Male','Male'),('Female','Female'))
nominee_r=(('Spouse','Spouse'),('Father','Father'),('Mother','Mother'),('Brother','Brother'),('Sister','Sister'),('Son','Son'),('Daughter','Daughter'),('Father-in-law','Father-in-law'),('Mother-in-law','Mother-in-law'))


class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default = "")
    member_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)  
    last_name = models.CharField(max_length=50)  
    email = models.EmailField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=15)
    alt_contact = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=15, choices=gender_select, blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    spouse_name = models.CharField(max_length=100, blank=True)
    nominee_name = models.CharField(max_length=100, blank=True)
    nominee_relation = models.CharField(max_length=100,choices=nominee_r, blank=True)
    nominee_address = models.CharField(max_length=200, blank=True)
    nominee_dob = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    sponsor_name = models.CharField(max_length=100, blank=True) 
    sponsor_id = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    pincode = models.CharField(max_length=7, blank=True)
    country = models.CharField(max_length=50, blank=True)
    join_date = models.DateField(auto_now_add=True, blank=True)
    join_amount = models.IntegerField(default=0)
    pan_number = models.CharField(max_length=10, blank=True)
    pan_image = models.FileField(upload_to="mymember/images",blank=True)
    adhaar_number = models.CharField(max_length=12, blank=True)
    adhaar_image = models.FileField(upload_to="mymember/images",blank=True)
    passport = models.CharField(max_length=20, blank=True)
    passport_image = models.FileField(upload_to="mymember/images",blank=True)
    voter_id = models.CharField(max_length=20, blank=True)
    voter_id_image = models.FileField(upload_to="mymember/images",blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    account_holder_name = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=20, blank=True)
    branch_name = models.CharField(max_length=20, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    branch_city = models.CharField(max_length=20, blank=True)
    passbook_image = models.FileField(upload_to="mymember/images",blank=True)
    cheque_image = models.FileField(upload_to="mymember/images",blank=True)
    position_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20,choices=profile_status, blank=True)
    activation_date = models.DateField(blank=True, null=True)
    user_image = models.ImageField(upload_to="mymember/images",blank=True)
    profile_validation = models.CharField(max_length=50,blank=True)
    position = models.CharField(max_length=20,blank=True)

    total_direct = models.IntegerField(default=0)
    total_indirect = models.IntegerField(default=0)
    team_size = models.IntegerField(default=1)
    direct_active = models.IntegerField(default=0)
    direct_inactive = models.IntegerField(default=0)
    total_inactive = models.IntegerField(default=0)
    swallet = models.IntegerField(default=0)
    ewallet = models.IntegerField(default=0)
    repurchase_income = models.IntegerField(default=0)
    direct_income = models.IntegerField(default=0)
    level_income = models.IntegerField(default=0)
    total_income = models.IntegerField(default=0)


    
  
    class Meta:  
        db_table = "MemberProfile"

    @property
    def full_name(self):
        return "%s %s"%(self.first_name, self.last_name)

    # def __str__(self):
    #     return self.full_name



class Product(models.Model):
    prod_id = models.AutoField
    prod_name = models.CharField(max_length=50,blank=True)
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    prod_desc = models.CharField(max_length=300,blank=True)
    pub_date = models.DateField(auto_now_add=True)
    prod_image = models.ImageField(upload_to="mymember/shop/images",blank=True)
    status = models.CharField(max_length=20,blank=True)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    member_id = models.CharField(max_length=20)
    name = models.CharField(max_length=90)
    amount = models.IntegerField(default=0)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, blank=True)
    delivery_status = models.CharField(max_length=20, blank=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    remarks = models.CharField(max_length=200, blank=True)
    

class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    

pay_for = [
    ('Join','Join'),
    ('Repurchase','Repurchase')
]

class Payment_Method(models.Model):
    payment_reference_no = models.CharField(max_length=50,blank=True)
    member_id = models.CharField(max_length=20,blank=True)
    payment_amount = models.IntegerField(default=0)
    payment_reason = models.CharField(max_length=50,blank=True,choices=pay_for)
    payment_type = models.CharField(max_length=20,blank=True)
    payment_slip_no = models.CharField(max_length=100,blank=True)
    payment_slip_image = models.ImageField(upload_to="mymember/payment",blank=True)
    payment_status = models.CharField(max_length=20,blank=True)
    payment_time = models.DateTimeField(auto_now_add=True,blank=True)
    payment_approval_time = models.DateTimeField(null=True,blank=True)
    comments = models.CharField(max_length=300,blank=True)
    income_added = models.CharField(max_length=20,blank=True)

    @property
    def full_name(self):
        return MemberProfile.objects.get(member_id=self.member_id).full_name
       

class Sponsor_Income(models.Model):
    payment_reference_no = models.CharField(max_length=50,blank=True)
    member_id = models.CharField(max_length=20,blank=True)
    member_income = models.IntegerField(default=0)
    monthly_pay = models.IntegerField(default=0)
    paid_amount = models.IntegerField(default=0)
    no_of_payment = models.IntegerField(default=0)
    payout_status = models.CharField(max_length=20,blank=True)
    responsible_id = models.CharField(max_length=20,blank=True)
    responsible_name = models.CharField(max_length=50,blank=True)
    join_amount=models.IntegerField(default=0)
    payout_date = models.DateField(null=True, blank=True)
    
    

class Repurchase_income(models.Model):
    payment_reference_no = models.CharField(max_length=50,blank=True)
    member_id = models.CharField(max_length=20,blank=True)
    member_income = models.IntegerField(default=0)
    bill_amount=models.IntegerField(default=0)
    income_type=models.CharField(max_length=50,blank=True) #l1,l2,l3
    payout_date = models.DateField(null=True, blank=True)
    payout_status = models.CharField(max_length=20,blank=True)
    responsible_id = models.CharField(max_length=20,blank=True)
    responsible_name = models.CharField(max_length=50,blank=True)


class Payout_summary(models.Model):
    payout_id = models.AutoField
    member_id = models.CharField(max_length=20,blank=True)
    member_name = models.CharField(max_length=50,blank=True)
    payout_amount = models.IntegerField(default=0)
    payout_reason = models.CharField(max_length=50,blank=True)
    payout_for = models.CharField(max_length=20,blank=True)
    payout_date = models.DateField(auto_now_add=True)
    responsible_id = models.CharField(max_length=20,blank=True)
    responsible_name = models.CharField(max_length=100,blank=True)
    payout_status = models.CharField(max_length=20,blank=True)
    payment_reference_no = models.CharField(max_length=50,blank=True)
    

