from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.admin_index, name='Admin_Home'),
    path('payment_status/<reference_no>', views.payment_status, name='Payment_Status'),
    path('search_member_<member_id>', views.search_member, name='Search_Member'),
    path('members', views.members_view, name='All_Member_View'),
    path('edit_<member_id>', views.members_edit, name='Member_Edit'),
    path('Processing...', views.payout_process, name='Payout_Process'),
    path('updating...', views.refresh, name='Refresh'),
    path('settings', views.settings_this, name='Settings'),
    path('GenaralHome', views.GenaralHome, name='GenaralHome'),
    path('MemberHome/<id>', views.Member_Home, name='MemberHome'),
    path('login', views.admin_login, name='Admin_Login'),
    path('logout', views.logout, name='Logout'),
    path('swallet_view', views.swallet_view, name='Swallet_View'),
    path('ewallet_view', views.ewallet_view, name='Ewallet_View'),
    path('withdraw_request_<number>', views.withdraw_request, name='Withdraw_Request'),
    path('add_Staff', views.staff_register,name="Staff_Register"),
    path('add_product_<id>', views.add_product,name="Add_Product"),
    path('product_list', views.product_list,name="Product_List"),
    path('downlines_<search_id>', views.downlines,name="Downlines"),
    path('this_month_sale', views.this_month_sale,name="This_Month_Sale"),
    path('sales_payments_summary', views.sales_payments_summary,name="Sales_Payments_Summary"),
    path('last_month_payout', views.last_month_payout,name="Last_Month_Payout"),
    path('ordering', views.ordering,name="Ordering"),

]
