from django import forms
from myAdmin.models import GeneralHome, MemberHome
from mymember.models import Payment_Method


class UpdateGeneralHome(forms.ModelForm):
    class Meta:
        model = GeneralHome
        fields = ['hightlightword','hightlight_descriptions','about_heading','about_descriptions','product_heading','product_heading_1',
        'product_desc_1','product_image_1','product_heading_2','product_desc_2','product_image_2','product_heading_3','product_desc_3','product_image_3',
        'product_heading_4','product_desc_4','product_image_4','glimpses_heading','glimpses_heading_1','glimpses_desc_1','glimpses_image_1','glimpses_heading_2',
        'glimpses_desc_2','glimpses_image_2','glimpses_heading_3','glimpses_desc_3','glimpses_image_3','glimpses_heading_4','glimpses_desc_4','glimpses_image_4',
        'glimpses_heading_5','glimpses_desc_5','glimpses_image_5','glimpses_heading_6','glimpses_desc_6','glimpses_image_6','offer_heading','offer_heading_1',
        'offer_desc_1','offer_image_1','offer_heading_2','offer_desc_2','offer_image_2','offer_heading_3','offer_desc_3','offer_image_3']

class UpdateMemberHome(forms.ModelForm):
    class Meta:
        model = MemberHome
        fields = ['status','slide_heading','slide_desc','slide_image','slide_heading']


class UpdatePayment_Status(forms.ModelForm):
    class Meta:
        model = Payment_Method
        fields = ['member_id','payment_amount','payment_reason','payment_type','payment_status','comments']