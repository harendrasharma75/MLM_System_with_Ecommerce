from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from mymember.models import AnonymousQuery
from mymember.forms import UserUpdationForm, UserImageForm, Kyc_Update, bank_Update
from django.contrib import auth
from django.contrib.auth.models import User
from mymember.models import MemberProfile, Product
from mymember.models import Payment_Method, Order, OrderUpdate, Payout_summary
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib import messages
from myAdmin.models import GeneralHome, MemberHome, Withdraw
import requests
import json
import random
from django.db.models import Sum



# Create your views here.
def sendPostRequest(phoneNo, textMessage):
    req_params = {
    'apikey':'WCZCE7W18OBVF2PA7TVA0KB8VFTAZ1AF', #This is API key for 9599024379
    'secret':"8SBBFMRQYQ1B85V2",  # This is secrete key for 9599024379
    'usetype':"stage", #This is usertype for live 'stage' and for testing 'prod'
    'phone': phoneNo,
    'message':textMessage,
    'senderid':'9599024379' # this is a sender id for www.sms4india.com
    }

    reqUrl = 'https://www.sms4india.com/api/v1/sendCampaign'
    return requests.post(reqUrl, req_params)

# get response
# response = sendPostRequest('Receiver mobile no.','text msg' )
#print(response.text)

def user(request):
    if request.user.get_username():
        username = request.user.get_username()
    else:
        username=None
    return username

def index(request):
    general = GeneralHome.objects.get(status='Active')
    
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('mobile')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        

        query =  AnonymousQuery(name=name, phone=phone, email=email, desc=desc, date=datetime.today())
        query.save()
        
        messages.warning(request,'Your query has been submitted successful. Our Team will call you sortly.')

    return render(request, 'index.html',{'general':general})

def team_update(member_id,id):#done
    member = MemberProfile.objects.get(member_id=member_id)
    x = member.team_size - member.total_inactive
    size = [0,5,20,100,500,1000,5000,100000]
    pos = ["New Joinee","Starter","Silver","Gold","Platinum","Diamond","God of Business"]
    for i in range(1,len(size)):
        if size[i-1] <= x <= size[i]:
            position = pos[i-1]
    
    member.position = position
    member.save()

    if  id == 1:
        self_member = MemberProfile.objects.filter(sponsor_id=member.member_id)
      
        member.total_direct = len(self_member)
        member.direct_active = len(MemberProfile.objects.filter(sponsor_id=member_id,status="Active"))
        member.direct_inactive = member.total_direct - member.direct_active
        member.total_inactive += 1
        member.team_size = member.total_direct + member.total_indirect + 1
        member.save()
        if member.member_id != 'JNHP00001':
            team_update(member.sponsor_id,2)  

    else:
        member.total_indirect += 1
        member.team_size += 1
        member.total_inactive += 1
        member.save()
        if member.member_id != 'JNHP00001':
            team_update(member.sponsor_id,2)
        

            
def reg(request,member_id):#done

    try:
        search=MemberProfile.objects.get(member_id=member_id)
        search_id = search.member_id
    except MemberProfile.DoesNotExist:
        search=None
        search_id=member_id

    context = {
        'search_id':search_id,
        'search':search
    }
    return render(request, 'register.html',context)


def register(request):#done
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        sponsor_id = request.POST.get('sponsor_id')
        sponsor_name = request.POST.get('sponsor_name')
        if sponsor_id=="":
            sponsor_name = 'Arun Sharma'
            sponsor_id = 'JNHP00001'
            ref_id = 'Starter'
        
        else:
            sub_member = MemberProfile.objects.filter(sponsor_id=sponsor_id)
            ref_id = str(len(sub_member)+1)

        password = request.POST.get('password')
        confirm_password = request.POST.get('password_confirmation')
             
        status = 'Inactive'

        if password == confirm_password:

            try:
                member = MemberProfile.objects.get(contact=contact)
                messages.warning(request,'Contact Number has been already registered.')
                return render(request,'register.html')
            except MemberProfile.DoesNotExist:            
                x = 0
                while x==0:
                    mem_id = "JNHP" + str(random.randint(1,99999)).rjust(5,'0')
                    try:
                        user = User.objects.get(username=mem_id)
                    
                    except User.DoesNotExist:
                        x=1
                    
                if email:
                    user = User.objects.create_user(username=mem_id, password=password, first_name=first_name, last_name=last_name,email=email)
                    user.save()
                    newmember = MemberProfile(member_id=mem_id, first_name=first_name,last_name=last_name,password=password,contact=contact,email=email,sponsor_id=sponsor_id,sponsor_name=sponsor_name,position_number=ref_id,status=status,user=user)
                else:
                    user = User.objects.create_user(username=mem_id, password=password, first_name=first_name, last_name=last_name)
                    user.save()
                    newmember = MemberProfile(member_id=mem_id, first_name=first_name,last_name=last_name,password=password,contact=contact,sponsor_id=sponsor_id,sponsor_name=sponsor_name,position_number=ref_id,status=status,user=user)
                
                newmember.save()
                team_update(newmember.sponsor_id,1)
                messages.success(request,f'Your registration has been successful.Your User ID is {mem_id}. Please login..')
                    
                    # response = sendPostRequest('9555663463',mem_id)
                    # print(response.text)
                return redirect('Login')
        else:
            messages.warning(request,'The password and confirmation password do not match.')
            return render(request,'register.html')
    



    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        member_id = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=member_id,password=password)

        if user is not None:
            auth.login(request,user)
            if request.GET.get('next',None):
                return redirect(request.GET['next'])

            messages.success(request,'You are logged in successfully.')
            return redirect('Dashboard')
        
        else:
            messages.warning(request,'Username or Password Incorrect.')
            return render(request,'login.html')


    return render(request, 'login.html')




@login_required(login_url='/login/')
def change_password(request):

    if request.user.get_username():
        username = request.user.get_username()
    else:
        username=None
    

    member = MemberProfile.objects.get(member_id= username)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            new_pass = request.POST.get('new_password1')
            member.password=new_pass
            member.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
            
    else:
        form = PasswordChangeForm(request.user)
        
    
    context = {
        'form':form,
        'member':member,
    }
    return render(request, 'change_password.html', context)



@login_required(login_url='/login')
def dashboard(request):
    

    member = MemberProfile.objects.filter(member_id=user(request))[0]

    
   
    
    reprchase_income = Payout_summary.objects.filter(member_id=member.member_id,payout_for='Repurchase').aggregate(Sum('payout_amount'))['payout_amount__sum']
    sponsored_income = Payout_summary.objects.filter(member_id=member.member_id,payout_for='Sponsor').aggregate(Sum('payout_amount'))['payout_amount__sum']
    level_income = Payout_summary.objects.filter(member_id=member.member_id,payout_for='Level Repurchase').aggregate(Sum('payout_amount'))['payout_amount__sum']

    if reprchase_income == None:
        reprchase_income = 0
    if sponsored_income == None:
        sponsored_income = 0
    if level_income == None:
        level_income = 0

    total_Earn = reprchase_income + sponsored_income + level_income

    kyc = [member.pan_number,member.pan_image,member.adhaar_number,member.adhaar_image,member.voter_id,member.voter_id_image]
    kyc_status = 10
    for i in kyc:
        if i != "":
            kyc_status += 15

    if request.method == "POST":
       
        form = UserImageForm(request.POST,request.FILES, instance = member) 
        
        if form.is_valid():  
            form.save()
            return redirect("Dashboard")
    
    actives = []
    acts = MemberHome.objects.filter(status='Active')
    
    n = len(acts)
    nSlides = n
    actives.append([acts,range(1,nSlides),nSlides])


    context = {
        'member':member,
        'actives':actives,
        'reprchase_income':reprchase_income,
        'sponsored_income': sponsored_income,
        'total_Earn':total_Earn,
        'level_income':level_income,
        'kyc_status':kyc_status,
    }
    return render(request, 'dashboard.html',context)


def logout(request):
    auth.logout(request)
    messages.warning(request,'You are logged out.')
    return redirect('Login')

@login_required(login_url='/login')
def profile(request):

    member = MemberProfile.objects.get(member_id=user(request))


    return render(request, 'profile.html',{'member':member})


    
@login_required(login_url='/login')
def edit(request):
    member = MemberProfile.objects.get(member_id=user(request))

    return render(request, 'editprofile.html',{'member':member})


@login_required(login_url='/login')
def upload_kyc(request):
    member = MemberProfile.objects.get(member_id=user(request))
    if request.method == "POST":
        form = Kyc_Update(request.POST,request.FILES, instance = member) 
        if form.is_valid():  
            form.save()
            messages.success(request,'KYC details has been submitted successfully.')
            return redirect("Upload_KYC")
        else:
        
            # print("errors : {}".format(form.errors))
            return redirect('Upload_KYC')

    return render(request, 'uploaddoc.html',{'member':member})


@login_required(login_url='/login')
def bank_details(request):
    member = MemberProfile.objects.get(member_id=user(request))
    if request.method == "POST":
        form = bank_Update(request.POST,request.FILES, instance = member) 
        if form.is_valid():  
            form.save()
            messages.success(request,'Bank details has been submitted successfully.')
            return redirect("Bank_details")
        else:
        
            # print("errors : {}".format(form.errors))
            return redirect('Bank_details')

    return render(request, 'bankdetails.html',{'member':member})


@login_required(login_url='/login')
def update(request):
    member = MemberProfile.objects.get(member_id=user(request))
    if request.method == "POST":
        form = UserUpdationForm(request.POST,request.FILES, instance = member) 
        if form.is_valid():  
            form.save()
            messages.success(request,'Profile has been updated successfully.')
            return redirect("Profile")
        else:
        
            # print("errors : {}".format(form.errors))
            return redirect('Profile_Edit')
    return render(request, 'editprofile.html',{'member':member})


@login_required(login_url='/login')
def addnew(request): #done
    if request.user.get_username():
        username = request.user.get_username()
    else:
        username=None
    
    member = MemberProfile.objects.get(member_id=username)
    sub_member = MemberProfile.objects.filter(sponsor_id=member.member_id)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        sponsor_name = request.POST.get('sponsor_name')
        sponsor_id = request.POST.get('sponsor_id')
        password = '12345'
        ref_id = str(len(sub_member)+1)
        status = 'Inactive'

        try:
            user = MemberProfile.objects.get(contact=contact)
            messages.warning(request,'Contact Number has been already registered.')
            return render(request,'addnewmember.html',{'member':member})
    
        except MemberProfile.DoesNotExist:
            
            x = 0
            while x==0:
                mem_id = "JNHP" + str(random.randint(1,99999)).rjust(5,'0')     
                try:
                    user = User.objects.get(username=mem_id)
                except User.DoesNotExist:
                    x=1

            if email:
                user = User.objects.create_user(username=mem_id, password=password, first_name=first_name, last_name=last_name,email=email)
                user.save()
                newmember = MemberProfile(member_id=mem_id, first_name=first_name,last_name=last_name,password=password,contact=contact,email=email,sponsor_id=sponsor_id,sponsor_name=sponsor_name,position_number=ref_id,status=status,user=user)
            else:
                user = User.objects.create_user(username=mem_id, password=password, first_name=first_name, last_name=last_name)
                user.save()
                newmember = MemberProfile(member_id=mem_id, first_name=first_name,last_name=last_name,password=password,contact=contact,sponsor_id=sponsor_id,sponsor_name=sponsor_name,position_number=ref_id,status=status,user=user)
  
            newmember.save()
            messages.success(request,f'You have added new Member successfully. New Member Id : {mem_id}')
                
            team_update(member.member_id,1)
                # response = sendPostRequest('9599024379',mem_id)
                # print(response.text)
            return redirect('Member_View')
      
    return render(request, 'addnewmember.html',{'member':member})   

@login_required(login_url='/login')
def with_request(request):
    if request.user.get_username():
        username = request.user.get_username()
    else:
        username=None
    
    member = MemberProfile.objects.get(member_id=username)
    payments = Withdraw.objects.filter(member_id=member.member_id)

    if request.method == "POST":
        name = member.full_name
        mem_id = member.member_id
        amount = request.POST.get('with_amt')
        status = 'Pending'
     
        x = 0
        a = 0
        while x==0:
            ref = Withdraw.objects.all()

            ref_id = 'PAY'+ str((len(ref)+a+1)).rjust(6,'0')

            try:
                pay = Withdraw.objects.get(request_no=ref_id)
                a += 1
            except Withdraw.DoesNotExist:
                x=1

        with_req = Withdraw(request_no=ref_id,member_name=name,member_id=mem_id,amount=amount,status=status)
        with_req.save()
        messages.success(request, f'Your request has been submitted successfully.')
        return redirect('With_Request')

    context = {
        'member':member,
        'payments':payments,
    }

    return render(request, 'with_request.html',context)    


@login_required(login_url='/login')
def memberview(request):
    member = MemberProfile.objects.filter(member_id=user(request))[0]
    sub_member = MemberProfile.objects.filter(sponsor_id=member.member_id)


    context = {
        'member': member,
        'sub_member':sub_member
    }
    
    return render(request,'memberview.html', context)

@login_required(login_url='/login')
def downline(request):
    member = MemberProfile.objects.filter(member_id=user(request))[0]
    sub_member = MemberProfile.objects.filter(sponsor_id=member.member_id)


    context = {
        'member': member,
        'sub_member':sub_member,
        'search_member':member
    }
    
    return render(request,'downline.html', context)

@login_required(login_url='/login')
def search_downline(request,search_id):
    member = MemberProfile.objects.filter(member_id=user(request))[0]
    search_member = MemberProfile.objects.get(member_id=search_id)
    sub_member = MemberProfile.objects.filter(sponsor_id=search_member.member_id)


    context = {
        'member': member,
        'search_member':search_member,
        'sub_member':sub_member,
    }
    
    return render(request,'downline.html', context)


from math import ceil

@login_required(login_url='/login')
def shop(request):
    member = MemberProfile.objects.filter(member_id=user(request))[0]
 
    allprods = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat,status="Active")
        if len(prod)==0:
            continue
        n = len(prod)
        nSlides = n//4 +ceil((n/4)-(n//4))
        allprods.append([prod,range(1,nSlides),nSlides])

    context = {
        'member':member,
        'allprods':allprods
    }
    return render(request,'shophome.html', context)


def search_product(request,member_id):
    return render(request,'shophome.html')

def view_product(request):

    return render(request,'shophome.html')

def product_view(request,id):
    member = MemberProfile.objects.get(member_id=user(request))

    product = Product.objects.filter(id=id)
    
    context = {
        'product':product[0],
        'member':member
    }
    return render(request,'product_veiw.html',context)



def tracker(request):
    member = MemberProfile.objects.get(member_id=user(request))
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
    
        try:
            order = Order.objects.filter(order_id=orderId)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                    print(response)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    context = {
        'member':member,
        
    }
    return render(request, 'tracker.html',context)



def welcome_letter(request):
    member = MemberProfile.objects.get(member_id=user(request))
    return render(request,'welcome.html',{'member':member})


def id_card(request):
    member = MemberProfile.objects.get(member_id=user(request))
    return render(request,'idcard.html',{'member':member})

def my_receipt(request):

    member = MemberProfile.objects.get(member_id=user(request))
   
    payments = Payment_Method.objects.filter(member_id=member.member_id,payment_status="Successful").order_by('-payment_time')
    
    context = {
        'member':member,
        'payments':payments
    }

    return render(request,'myreceipt.html',context)

def payout_receipt(request):

    member = MemberProfile.objects.get(member_id=user(request))
   

    payouts = Payout_summary.objects.filter(member_id=member.member_id,payout_status="Successful").values('payout_date').order_by('payout_date').annotate(sum=Sum('payout_amount'))
    invoice_no = str(member.member_id).replace('JNHP',"")

    context = {
        'member':member,
        'payouts':payouts,
        'invoice_no':invoice_no,
    }

    return render(request,'payoutreceipt.html',context)


def my_invoice(request):

    member = MemberProfile.objects.get(member_id=user(request))
   
    payouts = Payout_summary.objects.filter(member_id=member.member_id,payout_status="Successful").order_by('-payout_date')
    
    invoice = {}
    for i in payouts:
        if i.payout_date in invoice:
            invoice[i.payout_date].append([i.payout_reason,i.payout_amount])
        else:
            invoice[i.payout_date] = [[i.payout_reason,i.payout_amount]]
    
    
    
    x = Payout_summary.objects.filter(member_id=member.member_id,payout_status="Successful").values('payout_date').order_by('payout_date').annotate(sum=Sum('payout_amount'))
    
    datas = []
    for key in x:    
        if key['payout_date'] in invoice.keys():
            sums=[key['sum'], {key['payout_date'] : invoice[key['payout_date']]}]
            datas.append(sums)

    invoice_no = str(member.member_id).replace('JNHP',"")

    context = {
        'member':member,
        'payouts':payouts,
        'datas':datas,
        'invoice_no':invoice_no
    }

    return render(request,'myinvoice.html',context)


@login_required(login_url='/login')
def payment_details(request):
    member = MemberProfile.objects.get(member_id=user(request))
    if request.method == 'POST':
        x = 0
        a = 0
        while x==0:
            ref = Payment_Method.objects.all()

            ref_id = str((len(ref)+a+1)).rjust(7,'0')

            try:
                pay = Payment_Method.objects.get(payment_reference_no=ref_id)
                a += 1
            except Payment_Method.DoesNotExist:
                x=1
        
        pay_reason = request.POST.get('payment_reason')
        pay_type = request.POST.get('payment_type')
        pay_amt = request.POST.get('payment_amount')
        slip_no = request.POST.get('payment_slip_no')
        slip_img = request.FILES.get('payment_slip_image')
        pay_status = 'Pending'
        income_added = 'Unpaid'

        try:
            p = Payment_Method.objects.get(payment_slip_no=slip_no,payment_amount=pay_amt)
            messages.success(request,'Payment Slip No. has been already added. Please try with different slip no.')

        except Payment_Method.DoesNotExist:
            sub_pay = Payment_Method(payment_reference_no=ref_id,member_id=member.member_id,payment_amount=pay_amt,payment_reason=pay_reason,
            payment_type=pay_type,payment_slip_no=slip_no,payment_slip_image=slip_img,payment_status=pay_status,income_added=income_added)
        
            sub_pay.save()
            messages.success(request,'Payment Records has been submitted successfully. Payment staus change after received.')

    payments = Payment_Method.objects.filter(member_id=member.member_id)



    context = {
        'member':member,
        'payments':payments
    }
    return render(request,'paymentdetails.html',context)


@login_required(login_url='/login')
def payout_details(request):
    member = MemberProfile.objects.get(member_id=user(request))
    
    payouts = Payout_summary.objects.filter(member_id=member.member_id)

    invoice_no = str(member.member_id).replace('JNHP',"")

    context = {
        'member':member,
        'payouts':payouts,
        'invoice_no':invoice_no,
    }
    return render(request,'pay_sumary.html',context)


def calendar(request):
    member = MemberProfile.objects.get(member_id=user(request))
    return render(request,'calendar.html',{'member':member})



def checkout(request):
    member = MemberProfile.objects.get(member_id=user(request))
    id = None
    thank=False
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        member_id = request.POST.get('member_id', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('pin_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json,amount=amount,member_id=member_id, name=name, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        thank = True
        id = order.order_id
        return render(request, 'checkout.html', {'thank':thank, 'id': id})        
    
    context = {
        'member':member,
        'thank':thank, 
        'id': id
    }
    return render(request,'checkout.html',context)




def product_list(request):
    member = MemberProfile.objects.get(member_id=user(request))

    products = Product.objects.all()

    context = {
        'member':member,
        'products':products,
    }
    return render(request,'productlist.html',context)