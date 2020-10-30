from django.shortcuts import render, redirect
from mymember.models import Payment_Method,Sponsor_Income,Repurchase_income
from mymember.models import MemberProfile
from mymember.models import Payout_summary, Product
from myAdmin.models import admin_handle
from myAdmin.models import GeneralHome
from myAdmin.models import MemberHome, Withdraw, Staff_User
from myAdmin.forms import UpdateGeneralHome
from myAdmin.forms import UpdateMemberHome
from myAdmin.forms import UpdatePayment_Status
from mymember.forms import UserUpdationForm, bank_Update, Kyc_Update, UpdateProduct
from datetime import datetime
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
import random

# Create your views here.
def user(request):
    if request.user.get_username():
        username = request.user.get_username()
    else:
        username=None
    return username

def staff_register(request):
    
    if request.user.get_username():
        username = request.user.get_username()
    else:
        username=None
    
    user = User.objects.get(username=username)
    try:
        staff = Staff_User.objects.get(staff_id=username)

    except Staff_User.DoesNotExist:
        staff=None

    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        rights = request.POST.get('rights')
        designation = request.POST.get('designation')
        creator_name = request.POST.get('creator_name')
        creator_id = request.POST.get('creator_id')
        status = 'Inactive'
        x = 0
        a = 0
        while x==0:
            st_id = "ADMIN"+str(random.randint(1,999)).rjust(3,'0')
            try:
                user = User.objects.get(username=st_id)
            except User.DoesNotExist:
                x=1
        
        if user.is_superuser:
            if email:
                new_user = User.objects.create_user(username=st_id, password=st_id, first_name=f_name, last_name=l_name,email=email)
                if rights == "Full Rights":
                    new_user.is_superuser=True
                    new_user.is_staff=True
                else:
                    new_user.is_staff=True
                new_user.save()
                new_staff = Staff_User(staff_id=st_id,first_name=f_name, last_name=l_name,email=email,contact=contact,rights=rights,designation=designation,creator_id=creator_id,status=status,creator_name=creator_name,user=new_user)
            else:
                new_user = User.objects.create_user(username=st_id, password=st_id, first_name=f_name, last_name=l_name)
                if rights == "Full Rights":
                    new_user.is_superuser=True
                    new_user.is_staff=True
                else:
                    new_user.is_staff=True
                new_user.save()
                new_staff = Staff_User(staff_id=st_id,first_name=f_name, last_name=l_name,contact=contact,rights=rights,designation=designation,creator_id=creator_id,creator_name=creator_name,status=status,user=new_user)
            new_staff.save()
            messages.success(request,f'Staff registration has been successful.Your Staff ID is {st_id}.')
        
            return redirect('Admin_Home')

    return render(request,'myAdmin/staff_reg.html',{'staff':staff})

def admin_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        user = auth.authenticate(username=user_id,password=password)
        
        if user is not None:
            auth.login(request,user)
            if request.GET.get('next',None):
                return redirect(request.GET['next'])

            messages.success(request,'You are logged in successfully.')
            return redirect('Admin_Home')
            
        else:
            messages.warning(request,'Username or Password Incorrect.')
            return render(request,'myAdmin/adminlogin.html')

    return render(request,'myAdmin/adminlogin.html')

def logout(request):
    auth.logout(request)
    messages.warning(request,'You are logged out.')
    return redirect('Admin_Login')


@staff_member_required(login_url='/myAdmin/login')
def admin_index(request):

    pendings = Payment_Method.objects.filter(payment_status='Pending')

    total_balance = MemberProfile.objects.aggregate(Sum('swallet'))
    
    total_ewallet = MemberProfile.objects.aggregate(Sum('ewallet'))

    repurchase = Repurchase_income.objects.aggregate(Sum('member_income'))
    
    with_req = Withdraw.objects.filter(status = 'Pending')
    
    today_joining = MemberProfile.objects.filter(join_date=datetime.now().date())
    total_joinings =len(MemberProfile.objects.all())

    current_year = datetime.now().year
    current_month = datetime.now().month

    last_month_sale = Payment_Method.objects.filter(
        payment_approval_time__year__gte=current_year,
        payment_approval_time__month__gte=current_month,
        payment_status="Successful"
        ).aggregate(Sum('payment_amount'))

    last_month_payout = Payout_summary.objects.filter(
        payout_date__year__gte=current_year,
        payout_date__month__gte=current_month-1,
        ).aggregate(Sum('payout_amount'))

    admin = User.objects.get(username=user(request))
    user_staff = Staff_User.objects.get(staff_id=user(request))
    
    staffs = Staff_User.objects.all()
    
    if request.method == "POST":
        user_image = request.FILES.get('user_image')
        
        if user_image:
            user_staff.user_image=user_image
            user_staff.save()
            messages.success(request,'Image Uploaded Successfully.')
            return redirect("Admin_Home")

    total_pending = len(pendings)

    context = {
        
        'total_pending':total_pending,
        'total_balance':total_balance,
        'total_joinings':total_joinings,
        'today_joining': today_joining,
        'with_req':with_req,
        'last_month_sale':last_month_sale,
        'last_month_payout':last_month_payout,
        'staffs':staffs,
        'admin':admin,
        'user_staff':user_staff,
        'total_ewallet':total_ewallet,
    }

    return render(request,'myAdmin/admin_index.html',context)

def members_view(request):
    admin = User.objects.get(username=user(request))
    members = MemberProfile.objects.all()
    user_staff = Staff_User.objects.get(staff_id=user(request))
    context = {
        'members':members,
        'user_staff':user_staff,
        'admin':admin,
    }
    return render(request,'myAdmin/members.html',context)


def add_product(request,id):
    if id == "new":
        item = None
    else:
        item = Product.objects.get(id=id)

    admin = User.objects.get(username=user(request))
    products = Product.objects.all()
    user_staff = Staff_User.objects.get(staff_id=user(request))

    if request.method=="POST":
        id = request.POST.get("id")
        print(id)
        if id == "":
            prod = UpdateProduct(request.POST,request.FILES)
            if prod.is_valid():
                prod.save()
                messages.success(request,'Added successfully.')
        else:
            item = Product.objects.get(id=id)
            print(item.prod_name)
            prod = UpdateProduct(request.POST,request.FILES, instance = item)
            if prod.is_valid():
                prod.save()
                messages.success(request,'Updated successfully.')
        item = None

    context = {
        'products':products,
        'user_staff':user_staff,
        'admin':admin,
        'item':item,
    }
    return render(request,'myAdmin/addproducts.html',context)


def product_list(request):

    admin = User.objects.get(username=user(request))
    products = Product.objects.all()
    user_staff = Staff_User.objects.get(staff_id=user(request))

    
    context = {
        'products':products,
        'user_staff':user_staff,
        'admin':admin,
    }
    return render(request,'myAdmin/prodList.html',context)

def downlines(request,search_id):

    if search_id == "None":
        member = MemberProfile.objects.filter(member_id='JNHP00001')[0]
        search_member = MemberProfile.objects.get(member_id='JNHP00001')
    else:
        member = MemberProfile.objects.filter(member_id=search_id)[0]
        search_member = MemberProfile.objects.get(member_id=search_id)

    admin = User.objects.get(username=user(request))
    user_staff = Staff_User.objects.get(staff_id=user(request))
    
    
    sub_member = MemberProfile.objects.filter(sponsor_id=search_member.member_id)


    context = {
        'member': member,
        'search_member':search_member,
        'sub_member':sub_member,
        'user_staff':user_staff,
        'admin':admin,
    }
    
    return render(request,'myAdmin/DownLine.html', context)

def members_edit(request, member_id):
    try:
        member = MemberProfile.objects.get(member_id=member_id)
    except MemberProfile.DoesNotExist:
        member = None

    if request.method == "POST":
        form = UserUpdationForm(request.POST,request.FILES, instance = member)
        form1 = bank_Update(request.POST,request.FILES, instance = member)
        form2 = Kyc_Update(request.POST,request.FILES, instance = member)
        
        if form.is_valid() and form1.is_valid() and form2.is_valid():  
            form.save()
            form1.save()
            form2.save()
            messages.success(request,'Updated successfully.')
            return redirect('All_Member_View')
        # else:
        #     print("errors : {}".format(form.errors))

    user_staff = Staff_User.objects.get(staff_id=user(request))
    context = {
        'members':members,
        'user_staff':user_staff,
    }

    return render(request,'myAdmin/editMember.html',context)

def swallet_view(request):

    swallet = MemberProfile.objects.exclude(swallet__exact = 0)
    total_balance = MemberProfile.objects.aggregate(Sum('swallet'))
    user_staff = Staff_User.objects.get(staff_id=user(request))

    context = {
        'swallet':swallet,
        'total_balance':total_balance,
        'user_staff':user_staff,
    }
    return render(request,'myAdmin/swallet_bal.html',context)

def ewallet_view(request):

    ewallet = MemberProfile.objects.exclude(ewallet__exact = 0)
    total_balance = MemberProfile.objects.aggregate(Sum('ewallet'))
    user_staff = Staff_User.objects.get(staff_id=user(request))

    context = {
        'ewallet':ewallet,
        'total_balance':total_balance,
        'user_staff':user_staff,
    }
    return render(request,'myAdmin/ewallet_bal.html',context)

def this_month_sale(request):

    current_year = datetime.now().year
    current_month = datetime.now().month

    this_month = Payment_Method.objects.filter(
        payment_approval_time__year__gte=current_year,
        payment_approval_time__month__gte=current_month,
        payment_status="Successful"
        )

    sale = this_month.aggregate(Sum('payment_amount'))

    user_staff = Staff_User.objects.get(staff_id=user(request))

    context = {
        'this_month':this_month,
        'sale':sale,
        'user_staff':user_staff,
      
    }
    return render(request,'myAdmin/thismonthsale.html',context)


def sales_payments_summary(request):


    this_month = Payment_Method.objects.filter(payment_status="Successful")

    sale = this_month.aggregate(Sum('payment_amount'))

    user_staff = Staff_User.objects.get(staff_id=user(request))

    context = {
        'this_month':this_month,
        'sale':sale,
        'user_staff':user_staff,
      
    }
    return render(request,'myAdmin/sales_payment_summary.html',context)

def last_month_payout(request):

    current_year = datetime.now().year
    current_month = datetime.now().month

    last_month = Payout_summary.objects.filter(
        payout_date__year__gte=current_year,
        payout_date__month__gte=current_month-1,
        )

    payout = last_month.aggregate(Sum('payout_amount'))

    user_staff = Staff_User.objects.get(staff_id=user(request))

    context = {
        'last_month':last_month,
        'payout':payout,
        'user_staff':user_staff,
      
    }
    return render(request,'myAdmin/lastmonthpayout.html',context)

def withdraw_request(request,number):

    try:
        member = MemberProfile.objects.get(member_id=number)
        my_id = member.member_id
        req_no = None
    except MemberProfile.DoesNotExist:
        member = None
        try:
            req_no = Withdraw.objects.get(request_no=number)
            my_id = req_no.member_id
        except Withdraw.DoesNotExist:
            req_no = None
            my_id = ""
    
    if request.method == 'POST':
        
        member_id = request.POST.get('member_id')
        mem = MemberProfile.objects.get(member_id=member_id)
        amount = request.POST.get('amount')
        with_type = request.POST.get('with_type')
        remarks = request.POST.get('remarks')
        status = request.POST.get('status')
        request_no = request.POST.get('request_no')
        if request_no == "" or request_no == None:
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
            request_no = ref_id

            with_request = Withdraw(request_no=ref_id,member_name=mem.full_name,member_id=member_id,amount=amount,status=status)
            with_request.save()
        
        i = 0
        j = 0
        while i==0:
            r = Withdraw.objects.all()

            r_id = 'PAID'+ str((len(r)+j+1)).rjust(6,'0')

            try:
                paid = Withdraw.objects.get(withdraw_ref=r_id)
                j += 1
            except Withdraw.DoesNotExist:
                i=1
        withdraw_ref = r_id
        
        withdraw = Withdraw.objects.get(request_no=request_no)
        if status == "Successful" or status == "Rejected":      
            if status == "Successful":
                withdraw.withdraw_ref = withdraw_ref
                withdraw.with_type = with_type
                mem.ewallet -= int(amount)
                mem.save()
                
            withdraw.status = status
            withdraw.withdraw_date = datetime.now()
            withdraw.remarks = remarks
            withdraw.save()
            messages.success(request,f'Updated Successfully.')


    with_req = Withdraw.objects.filter(status = 'Pending')
    total_balance = with_req.aggregate(Sum('amount'))
    print(total_balance)
    with_his = Withdraw.objects.exclude(status__exact = 'Pending')
   
    user_staff = Staff_User.objects.get(staff_id=user(request))

    context = {
        'with_req':with_req,
        'total_balance':total_balance,
        'with_his':with_his,
        'member':member,
        'req_no':req_no,
        'my_id':my_id,
        'user_staff':user_staff,
    }
    return render(request,'myAdmin/withdraw_req.html',context)

def search_member(request,member_id):#done
    try:
        search=MemberProfile.objects.get(member_id=member_id)
        edit = Payment_Method.objects.filter(member_id=member_id)
        edit.payment_reference_no = None
    except MemberProfile.DoesNotExist:
        search=None
        edit=None

    pendings = Payment_Method.objects.filter(payment_status='Pending')
    successs = Payment_Method.objects.filter(payment_status='Successful')
    rejects = Payment_Method.objects.filter(payment_status='Rejected')
    my_id = member_id

    user_staff = Staff_User.objects.get(staff_id=user(request))

    context = {
        'edit':edit,
        'my_id':my_id,
        'search':search,
        'pendings':pendings,
        'successs':successs,
        'rejects':rejects, 
        'user_staff':user_staff,     
    }
    return render(request,'myAdmin/pending_payment.html',context)
    
def active_change(member_id,id):#done
    member = MemberProfile.objects.get(member_id=member_id)

    x = member.team_size - member.total_inactive
    size = [0,5,20,100,500,1000,5000,100000]
    pos = ["New Joinee","Starter","Silver","Gold","Platinum","Diamond","God of Business"]
    for i in range(1,len(size)):
        if size[i-1] <= x <= size[i]:
            position = pos[i-1]
    
    member.position = position
    member.save()
    
    if id == 1:
        member.direct_active = len(MemberProfile.objects.filter(sponsor_id=member_id,status="Active"))
        member.direct_inactive = len(MemberProfile.objects.filter(sponsor_id=member_id,status="Inactive"))
        member.total_inactive -= 1
        member.save()
        if member.member_id != 'JNHP00001':
            active_change(member.sponsor_id,2)

    else:
        member.total_inactive -= 1
        member.save()
        if member.member_id != 'JNHP00001':
            active_change(member.sponsor_id,2)
       


def payment_status(request,reference_no):#done
    try:

        edit = Payment_Method.objects.get(payment_reference_no=reference_no)
        my_id=edit.member_id
       
        # if edit.payment_status=='Successful':
        #     edit=None
            

    except Payment_Method.DoesNotExist:
        edit = None
        my_id=""


    if request.method == "POST":
        if edit==None:
            x = 0
            a=0
            while x==0:
                ref = Payment_Method.objects.all()
                reference_no = str((len(ref)+1+a)).rjust(7,'0')
                try:
                    pay = Payment_Method.objects.get(payment_reference_no=reference_no)
                    a+=1
                except Payment_Method.DoesNotExist:
                    x=1  

            subpay = Payment_Method(payment_reference_no=reference_no)
            subpay.save()

        edit = Payment_Method.objects.get(payment_reference_no=reference_no) 
        form = UpdatePayment_Status(request.POST,instance = edit)
        if form.is_valid():
            form.save()
            edit = Payment_Method.objects.get(payment_reference_no=reference_no)
            edit.payment_approval_time = datetime.now()
            edit.income_added = "Unpaid"
            edit.save()

            messages.success(request,f'Submited Successfully.')
      
        if edit.payment_reason == 'Join' and edit.payment_status=='Successful':
            member = MemberProfile.objects.get(member_id=edit.member_id)
            member.status='Active'
            member.join_amount=edit.payment_amount
            member.activation_date=datetime.now()
            member.save()
            active_change(member.sponsor_id,1)
        edit = None

        return redirect("Payment_Status",edit)

   

    pendings = Payment_Method.objects.filter(payment_status='Pending')
    successs = Payment_Method.objects.filter(payment_status='Successful')
    rejects = Payment_Method.objects.filter(payment_status='Rejected')
    user_staff = Staff_User.objects.get(staff_id=user(request))
    context = {
        'my_id':my_id,
        'edit':edit,
        'pendings':pendings,
        'successs':successs,
        'rejects':rejects,
        'user_staff':user_staff
        
        
    }
    return render(request,'myAdmin/pending_payment.html',context)

def payout_process(request):
    admin_set = admin_handle.objects.get(user_name='admin')
    repurchase_payout = Repurchase_income.objects.filter(payout_status="IP")
    for r in range(len(repurchase_payout)):
        member = MemberProfile.objects.get(member_id=repurchase_payout[r].member_id)
        if int((repurchase_payout[r].income_type).split('_')[-1])==1:
            p_for = "Repurchase"
        else:
            p_for = "Level Repurchase"
        payout_r = Payout_summary(
            member_id = member.member_id,
            member_name = member.full_name,
            payout_amount = repurchase_payout[r].member_income,
            payout_reason = repurchase_payout[r].income_type + " for " + repurchase_payout[r].responsible_name,
            payout_for = p_for,
            responsible_id = repurchase_payout[r].responsible_id,
            responsible_name = repurchase_payout[r].responsible_name,
            payout_status = "Successful",
            payment_reference_no = repurchase_payout[r].payment_reference_no,
        )
        payout_r.save()
        repurchase_payout[r].payout_date = datetime.today()
        repurchase_payout[r].payout_status = "Paid"
        repurchase_payout[r].save()
        member.ewallet += (payout_r.payout_amount-payout_r.payout_amount*admin_set.tax_gst/100)
        member.swallet -= payout_r.payout_amount
        member.save()

    
    sponsor_payout = Sponsor_Income.objects.filter(payout_status="IP")
    for p in range(len(sponsor_payout)):
        if (datetime.today().date()-sponsor_payout[p].payout_date).days >= 24:
            member = MemberProfile.objects.get(member_id=sponsor_payout[p].member_id)
            payout_s = Payout_summary(
                member_id = member.member_id,
                member_name = member.full_name,
                payout_amount = sponsor_payout[p].monthly_pay,
                payout_reason = "Sponsor Income :"+ str(11-sponsor_payout[p].no_of_payment) + " for " + sponsor_payout[p].responsible_name,
                payout_for = "Sponsor",
                responsible_id = sponsor_payout[p].responsible_id,
                responsible_name = sponsor_payout[p].responsible_name,
                payout_status = "Successful",
                payment_reference_no = sponsor_payout[p].payment_reference_no,
            )
            payout_s.save()
            sponsor_payout[p].payout_date = datetime.today()
            sponsor_payout[p].paid_amount += sponsor_payout[p].monthly_pay
            sponsor_payout[p].no_of_payment -= 1
            if sponsor_payout[p].no_of_payment == 0:
                sponsor_payout[p].payout_status = "Paid"
            sponsor_payout[p].save()
            member.ewallet += (payout_s.payout_amount-payout_s.payout_amount*admin_set.tax_gst/100)
            member.swallet -= payout_s.payout_amount
            member.save()
    
    return redirect("Admin_Home")


def level_income(lvl, member_id, amount, ref, pur_id):
    admin_set = admin_handle.objects.get(user_name='admin')
    purchase_income = [admin_set.l1_income, admin_set.l2_income, admin_set.l3_income, admin_set.l4_income, admin_set.l5_income,
    admin_set.l6_income,admin_set.l7_income, admin_set.l8_income, admin_set.l9_income]

    member = MemberProfile.objects.get(member_id=member_id)
    resp_id = MemberProfile.objects.get(member_id=pur_id)

    purchase_income_add = Repurchase_income(
        payment_reference_no = ref,
        member_id = member_id,
        member_income = amount*purchase_income[lvl-1]/100,
        bill_amount= amount,
        income_type = 'Level_'+str(lvl),
        payout_status = "IP",
        responsible_id = resp_id.member_id,
        responsible_name = resp_id.full_name,
    )
    purchase_income_add.save()
    member.swallet += purchase_income_add.member_income
    member.save()

   
def refresh(request):
    admin_set = admin_handle.objects.get(user_name='admin')
   
    spon_income = Payment_Method.objects.filter(income_added='Unpaid',payment_reason='Join',payment_status='Successful')
    for i in range(len(spon_income)):
        self_id = MemberProfile.objects.get(member_id=spon_income[i].member_id)
        sponsor = MemberProfile.objects.get(member_id=self_id.sponsor_id)
        if spon_income[i].payment_approval_time.day >= 15:
            x = 10
        else:
            x = 1
        s = str(spon_income[i].payment_approval_time.year)+"-"+str(spon_income[i].payment_approval_time.month)+"-"+str(x)
        pay_date = datetime.strptime(s, "%Y-%m-%d").date()

        sponsor_income_add = Sponsor_Income(
            payment_reference_no = spon_income[i].payment_reference_no,
            member_id = sponsor.member_id,
            member_income = admin_set.spon_income * admin_set.spon_month_income,
            monthly_pay = admin_set.spon_income,
            no_of_payment = admin_set.spon_month_income,
            payout_status = "IP",
            responsible_id = self_id.member_id, 
            responsible_name = self_id.full_name,
            join_amount = spon_income[i].payment_amount,
            payout_date = pay_date,
            )
        sponsor_income_add.save()
        spon_income[i].income_added = "Paid"
        spon_income[i].save()
        sponsor.swallet += sponsor_income_add.member_income
        sponsor.save()

    l_income = Payment_Method.objects.filter(income_added='Unpaid',payment_reason='Repurchase',payment_status='Successful')
    for j in range(len(l_income)):
        amt = l_income[j].payment_amount
        ref = l_income[j].payment_reference_no
        pur_id = l_income[j].member_id
        earn_id = MemberProfile.objects.get(member_id=l_income[j].member_id)
        leve = admin_set.lvl_income
        for lvl in range(1,leve+1):
            mem_id = earn_id.member_id
            level_income(lvl,mem_id,amt,ref,pur_id)
            if earn_id.sponsor_id == "JNHP00001":
                break
            earn_id = MemberProfile.objects.get(member_id=earn_id.sponsor_id)
        l_income[j].income_added = "Paid"
        l_income[j].save()

    return redirect('Admin_Home')


def settings_this(request):
    return render(request,'myAdmin/settings.html')


def GenaralHome(request):
    general = GeneralHome.objects.get(status='Active')
    if request.method == "POST":
        form = UpdateGeneralHome(request.POST,request.FILES, instance = general) 
        if form.is_valid():
            form.save()
            general.latest_date = datetime.now()
            general.save()
            messages.success(request,'General Home has been updated successfully.')
            return redirect("GenaralHome")
        else:
            
            # print("errors : {}".format(form.errors))
            return redirect("GenaralHome")

    return render(request,'myAdmin/GenaralHome.html',{'general':general})

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def Member_Home(request,id):

    if is_integer(id):
        id=id
    else:
        id=-1
    try:
        
        general = MemberHome.objects.get(id=int(id))
        
    except MemberHome.DoesNotExist:
        general=None

    if request.method == "POST":
        if  general==None:
            form = UpdateMemberHome(request.POST,request.FILES)
        else:
            form = UpdateMemberHome(request.POST,request.FILES,instance = general)
        if form.is_valid():
            form.save()
            general=None
            messages.success(request,'General Home has been updated successfully.')
            return redirect("MemberHome",general)
        else:
        
            # print("errors : {}".format(form.errors))
            return redirect("MemberHome",general)
    
    actives = MemberHome.objects.filter(status='Active')
    inactives = MemberHome.objects.filter(status='Inactive')

    cotext = {
        'actives':actives,
        'inactives':inactives,
        'general':general
    }

    return render(request,'myAdmin/MemberHome.html',cotext)

def ordering(request):
    products = Product.objects.all()

    context = {
        'products':products,
    }

    return render(request,'myAdmin/ordering.html', context)