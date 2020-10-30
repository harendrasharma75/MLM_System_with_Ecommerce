from django import forms  
from django.contrib.auth.models import User
from mymember.models import MemberProfile, Payment_Method, Product

from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import UserUpdationForm


profile_status=(('Active','Active'),('Inactive','Inactive'))
gender_select=(('Male','Male'),('Female','Female'))
nominee_r=(('Spouse','Spouse'),('Father','Father'),('Mother','Mother'),('Brother','Brother'),('Sister','Sister'),('Son','Son'),('Daughter','Daughter'),('Father-in-law','Father-in-law'),('Mother-in-law','Mother-in-law'))



class UserUpdationForm(forms.ModelForm):
   
    class Meta:  
        model = MemberProfile 
        # fields = '__all__' 
        fields = ['first_name','last_name','email','contact','alt_contact','gender','father_name','spouse_name','nominee_name',
        'nominee_relation','nominee_address','nominee_dob','date_of_birth','sponsor_name','sponsor_id','password','address','city','state','pincode','country',
        'position_number','status','activation_date','user_image'] #https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = {
            'first_name' : forms.TextInput(attrs={ 'class': 'form-control' }),  
            'last_name' : forms.TextInput(attrs={ 'class': 'form-control' }),  
            'email' : forms.EmailInput(attrs={ 'class': 'form-control' }),  
            'contact' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'alt_contact' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'gender' : forms.Select(attrs={ 'class': 'form-control' }, choices=gender_select),
            'father_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'spouse_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'nominee_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'nominee_relation': forms.TextInput(attrs={ 'class': 'form-control' }),
            'nominee_address': forms.TextInput(attrs={ 'class': 'form-control' }),
            'nominee_dob': forms.DateInput(attrs={ 'class': 'form-control' }),
            'date_of_birth' : forms.DateInput( attrs={ 'class': 'form-control' }),
            'sponsor_name': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'sponsor_id': forms.TextInput(attrs={ 'class': 'form-control' }),
            'password': forms.TextInput(attrs={ 'class': 'form-control' }),
            'address': forms.TextInput(attrs={ 'class': 'form-control' }),
            'city': forms.TextInput(attrs={ 'class': 'form-control' }),
            'state': forms.TextInput(attrs={ 'class': 'form-control' }),
            'pincode': forms.TextInput(attrs={ 'class': 'form-control' }),
            'country': forms.TextInput(attrs={ 'class': 'form-control' }),

            'position_number' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'status' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'activation_date' : forms.DateInput(attrs={ 'class': 'form-control' }),
            'user_image' : forms.FileInput(attrs={ 'class': 'form-control' }),
            }

class Kyc_Update(forms.ModelForm):
    class Meta:  
        model = MemberProfile 
        fields = ['pan_number','pan_image','adhaar_number','adhaar_image','passport','passport_image','voter_id','voter_id_image',]
        widgets = {'pan_number' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'pan_image':forms.FileInput(attrs={ 'class': 'form-control' }),
            'adhaar_number' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'adhaar_image':forms.FileInput(attrs={ 'class': 'form-control' }),
            'passport' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'passport_image':forms.FileInput(attrs={ 'class': 'form-control' }),
            'voter_id' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'voter_id_image':forms.FileInput(attrs={ 'class': 'form-control' }),
            }

class bank_Update(forms.ModelForm):
    class Meta:  
        model = MemberProfile 
        fields = ['account_number','account_holder_name','bank_name','branch_name','ifsc_code','branch_city','passbook_image','cheque_image']
        widgets = {
            'account_number' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'account_holder_name' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'bank_name' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'branch_name' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'ifsc_code' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'branch_city' : forms.TextInput(attrs={ 'class': 'form-control' }),
            'passbook_image':forms.FileInput(attrs={ 'class': 'form-control' }),
            'cheque_image':forms.FileInput(attrs={ 'class': 'form-control' }),
            }

class UserImageForm(forms.ModelForm):
   
    class Meta:  
        model = MemberProfile 
        fields = ['user_image']
        widgets = {'user_image' : forms.FileInput(attrs={ 'class': 'form-control' }),
            }


class AddNewForm(forms.ModelForm):
   
    class Meta:  
        model = MemberProfile 
        fields = ['first_name','last_name','contact','email','sponsor_name','sponsor_id']
        widgets = {'first_name': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'last_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'email': forms.EmailInput(attrs={ 'class': 'form-control' }),
            'contact': forms.EmailInput(attrs={ 'class': 'form-control' }),
            'sponsor_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'sponsor_id': forms.TextInput(attrs={ 'class': 'form-control' }),
            
            }


pay_for = [
    ('Join','Join'),
    ('Repurchase','Repurchase')
] 


class UpdateProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['prod_name','category','sub_category','price','prod_desc','status','prod_image']