from django.urls import path, include
from . import views
# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='Home'),
    path('login', views.login, name='Login'),
    path('new_user', views.register, name='Register'),
    path('new_user_sponsor_<member_id>', views.reg, name='Reg'),
    path('dashboard', views.dashboard, name='Dashboard'),
    path('logout', views.logout, name='Logout'),
    path('profile', views.profile, name='Profile'),
    path('profile_edit', views.edit, name='Profile_Edit'),
    path('profile_update', views.update, name='Profile_Update'),
    path('addnewmember', views.addnew, name='Add_New'),
    path('memberview', views.memberview, name='Member_View'),
    path('downline', views.downline, name='Downline_View'),
    path('downline_<search_id>', views.search_downline, name='Downline_Search'),
    path('shop', views.shop, name='Shop'),
    path('products/<int:id>', views.product_view, name='Product_View'),
    path('search', views.search_product, name='Shop_Product'),
    path('product_view', views.view_product, name='Product_View'),
    path('checkout', views.checkout, name='CheckOut'),
    path('track_order', views.tracker, name='Tracker'),
    path('welcome_letter', views.welcome_letter, name='Welcome_Letter'),
    path('id_card', views.id_card, name='ID_Card'),
    path('my_receipt', views.my_receipt, name='My_Receipt'),
    path('payout_receipt', views.payout_receipt, name='Payout_Receipt'),
    path('my_invoice', views.my_invoice, name='My_Invoice'),
    path('payment_details', views.payment_details, name='Payment_Details'),
    path('payout_details', views.payout_details, name='Payout_Details'),
    path('upload_kyc', views.upload_kyc, name='Upload_KYC'),
    path('edit_bank', views.bank_details, name='Bank_details'),
    path('password', views.change_password, name='change_password'),
    path('calendar', views.calendar, name='Calendar'),

    path('products', views.product_list, name='Product_List'),
    path('withdraw_request', views.with_request, name='With_Request'),
    
]
# + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    