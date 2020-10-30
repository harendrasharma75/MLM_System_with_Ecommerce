from django.contrib import admin

from mymember.models import AnonymousQuery
from mymember.models import MemberProfile
from mymember.models import Product
from mymember.models import Payment_Method
from mymember.models import Sponsor_Income
from mymember.models import Repurchase_income
from mymember.models import Payout_summary
from mymember.models import Order, OrderUpdate




# Register your models here.
admin.site.register(OrderUpdate)
admin.site.register(AnonymousQuery)
admin.site.register(Order)



@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("member_id", "full_name",'position', 'email','contact','alt_contact','gender','date_of_birth','father_name','spouse_name','nominee_name',
        'nominee_relation','nominee_address','nominee_dob','sponsor_name','sponsor_id','password','address','city','state','pincode','country',
        'pan_number','pan_image','adhaar_number','adhaar_image','passport','passport_image','voter_id','voter_id_image','account_number','account_holder_name','bank_name',
        'branch_name','ifsc_code','position_number','join_date','join_amount','status','activation_date','user_image',
        'total_direct','direct_active','direct_inactive','total_indirect','total_inactive','team_size',
        'swallet','ewallet')



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('prod_name','prod_desc','pub_date')


@admin.register(Payment_Method)
class Payment_MethodAdmin(admin.ModelAdmin):
    list_display=('payment_reference_no','member_id','payment_amount','payment_reason','payment_type','payment_slip_no','payment_slip_image',
    'payment_status','payment_time','payment_approval_time','comments','income_added')


@admin.register(Sponsor_Income)
class Sponsor_IncomeAdmin(admin.ModelAdmin):
    list_display=('payment_reference_no','member_id','member_income','monthly_pay','paid_amount','no_of_payment','payout_status','responsible_id',
    'responsible_name','join_amount','payout_date')


@admin.register(Repurchase_income)
class Repurchase_incomeAdmin(admin.ModelAdmin):
    list_display=('payment_reference_no','member_id','member_income','bill_amount','income_type','payout_date',
    'payout_status','responsible_id','responsible_name')

@admin.register(Payout_summary)
class Payout_summaryAdmin(admin.ModelAdmin):
    list_display = ('member_id','member_name','payout_amount','payout_reason','payout_for','payout_date','responsible_id','responsible_name','payout_status','payment_reference_no')