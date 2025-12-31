from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponse
from .models import CustomUser
from django.contrib.auth import login
# Create your views here.




def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.is_active = False
            user.save()
            
            # activation link
            current_site = get_current_site(request) # http://127.0.0.1/
            email = user.email
            subject = "Verify Email"
            message = render_to_string('user/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            }
            )
            
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
           
            return HttpResponse('Please, verify your gmail')
        
            
    return render(request,'user/register.html',{'form':form})   



def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    print('----------------------')
    print(user)
    print('----------------------')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        login(request,user , backend='django.contrib.auth.backends.ModelBackend')        
        return redirect('upskill:index')
    else:
        messages.warning(request, 'The link is invalid.')
        return HttpResponse('Oops, smth is wrong')
      
      
