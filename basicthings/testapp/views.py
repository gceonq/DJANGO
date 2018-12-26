from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm ,in function UserCreationForm changed to RegistrationForm (forms.py)
#from django.contrib.auth.forms import UserChangeForm   ,'in function UserChangeForm changed to EditProfileForm (forms.py)
#from testapp.forms import RegistrationForm             , b'cz we are using customized form ,commented in forms.py file

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, authenticate        #used to direct login after signup
from  django.contrib.auth import update_session_auth_hash  #session to continue even after changing the password
from testapp.forms import UserCreationForm,EditProfileForm
from django.core.mail import send_mail
from django.conf import settings


from django.contrib.auth.models import User
from django.contrib import auth

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from testapp.tokens import account_activation_token
from django.core.mail import EmailMessage

from django.contrib import messages


# Create your views here.
def baseview(request):

    return render(request,'testapp/base.html')
@login_required
def loginview(request):

    return render(request,'testapp/thankslogin.html')

"""
this register function is default signup function
email value is not taking,so we go for customised one below
"""
# def register(request):    #to implement this we have to edit forms.py
#     if request.method =='POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request,'testapp/thankssignup.html')
#     else:
#         form = RegistrationForm()
#
#
#     return render(request,'testapp/reg_form.html',{'form':form})

def register(request):
     if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             username = form.cleaned_data['username']
             first_name = form.cleaned_data['first_name']
             last_name = form.cleaned_data['last_name']
             email = form.cleaned_data['email']
             password = form.cleaned_data['password']
             user = User.objects.create_user(username=username,first_name=first_name,last_name =last_name,email=email,password=password)
             user.is_active = False
             user.save()

             #
             # #usr = auth.authenticate(username=username,password=password)
             # #auth.login(request,usr)                                        #if need,this should be done after user.is_active = True,
             # #return render(request,'testapp/thankslogin.html')              #if email verification is necessary then no need to place these three lines

             # pk = user.id                                                     #to know the id of the registering user
             # print("primary key : ",pk)

             # subject = 'Thanks for your registration'                         #manually sending the mail,never recommended
             # message = """Welcome to python.
             # click on this link to activate your account.
             # http://127.0.0.1:8000/testapp/activateview/"""+ str(pk)
             # from_email = settings.EMAIL_HOST_USER
             # to_list = [user.email,settings.EMAIL_HOST_USER]
             # send_mail(subject,message,from_email,to_list,fail_silently=True)

             current_site = get_current_site(request)
             message = render_to_string('testapp/acc_active_email.html', {
                 'user': user,
                 'domain': current_site.domain,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': account_activation_token.make_token(user),
             })
             mail_subject = 'Activate your blog account.'
             to_email = form.cleaned_data.get('email')
             email = EmailMessage(mail_subject, message, to=[to_email])
             email.send()


             return render(request, 'testapp/thanks_confirmation.html')

         #return HttpResponseRedirect('accounts/login')                 #for direct login
     else:
         form = UserCreationForm()

     return render(request,'testapp/reg_form.html',{'form':form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return render(request, 'testapp/thankssignup.html')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # return render(request, 'login.html', {'form': form})
    else:

     return HttpResponse('Activation link is invalid!')




# def activate_view(request,pk):                                #this activate view for manually configured mail verification
#     user = User.objects.get(pk=pk)
#     user.is_active=True
#     user.save()
#     return render(request,'testapp/thankssignup.html')

@login_required
def view_profile(request):
    storage = messages.get_messages(request)
    args={'user':request.user,'message':storage}

    return render(request,'testapp/profile.html',args)

@login_required
def edit_profile(requset):
    if requset.method == 'POST':
        form = EditProfileForm(requset.POST,instance=requset.user)

        if form.is_valid():
            form.save()
            return redirect('/testapp/profile')
    else:
        form = EditProfileForm(instance=requset.user)

    return render(requset,'testapp/edit_profile.html',{'form':form})

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST,user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request,'your password has been changed')
            update_session_auth_hash(request,form.user)
            return redirect('/testapp/profile')
        else:
            return redirect('/testapp/changepassword')
    else:

        form = PasswordChangeForm(user=request.user)

    return render(request,'testapp/change_password.html',{'form' : form})



def password_info(request):

    return render(request,'testapp/password_info.html')
