from django.contrib import admin

# Register your models here.
from myAdmin.models import admin_handle, GeneralHome, MemberHome, Withdraw, Staff_User

admin.site.register(GeneralHome)
admin.site.register(MemberHome)

@admin.register(admin_handle)
class admin_handleAdmin(admin.ModelAdmin):
    list_display = ('user_name','admin_charge','tax_gst','spon_income','spon_month_income','l1_income','l2_income','l3_income','bonus','next_payout_date')


@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    list_display =('request_no','member_name','member_id','amount','status','request_date','with_type','withdraw_ref','withdraw_date','remarks')

@admin.register(Staff_User)
class Staff_UserAdmin(admin.ModelAdmin):
    list_display=('staff_id','first_name','last_name','contact','email','rights','designation','creator_name','creator_id','user_image','status',
    'address','city','pin','state','pan_number','pan_image','adhaar_number','adhaar_image','passport','passport_image','voter_id','voter_id_image',
    'account_number','account_holder_name','bank_name','branch_name','ifsc_code','branch_city','passbook_image','cheque_image')





