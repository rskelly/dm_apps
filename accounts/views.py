from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash, login
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, UpdateView, CreateView, \
    FormView  # ,ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .tokens import account_activation_token
from . import forms
from . import emails
from . import models
from .auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token
from .graph_helper import get_user


def sign_in(request):
    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url()
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)


def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)

    # Get the user's profile
    user = get_user(token)
    my_email = user.get("mail")
    try:
        my_user = User.objects.get(email__iexact=my_email)
    except User.DoesNotExist:
        my_first_name = user.get("givenName")
        my_last_name = user.get("surname")
        my_user = User.objects.create(
            username=my_email,
            email=my_email,
            first_name=my_first_name,
            last_name=my_last_name,
            is_active=True,
            password="pbkdf2_sha256$120000$ctoBiOUIJMD1$DWVtEKBlDXXHKfy/0wKCpcIDYjRrKfV/wpYMHKVrasw=",
        )
    login(request, my_user)
    return HttpResponseRedirect(reverse('index'))


class CloserTemplateView(TemplateView):
    template_name = 'accounts/close_me.html'


def access_denied(request):
    my_url = reverse("accounts:request_access")
    a_tag = mark_safe('<a pop-href="{}" href="#" class="request-access-button">this</a>'.format(my_url))
    denied_message = "Sorry, you are not authorized to view this page. You can request access using {} form.".format(
        a_tag)
    messages.error(request, mark_safe(denied_message))
    # send user back to the page that they came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def access_denied_custodian(request):
    denied_message = "Sorry, only custodians and system administrators have access to this view."
    messages.error(request, denied_message)
    # send user back to the page that they came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def access_denied_adm(request):
    denied_message = "Sorry, only ADMO administrators can verify projects that require ADM approval."
    messages.error(request, denied_message)
    # send user back to the page that they came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def access_denied_project_leads_only(request):
    denied_message = _("Sorry, you do not have the necessary permissions to access to this page.")
    messages.error(request, denied_message)
    # send user back to the page that they came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def access_denied_section_heads_only(request):
    denied_message = _("Sorry, you need to be a manager of this project in order to access this page.")
    messages.error(request, denied_message)
    # send user back to the page that they came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def access_denied_manager_or_admin_only(request):
    denied_message = _("Sorry, you need to be a manager or site admin in order to access this page.")
    messages.error(request, denied_message)
    # send user back to the page that they came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def access_denied_scifi(request):
    denied_message = "Sorry, you do not have the permissions to modify this record."
    messages.error(request, denied_message)
    # send user back to the page that they came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProfileUpdateView(UpdateView):
    model = models.Profile
    form_class = forms.ProfileForm
    success_url = "#"

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs['pk'])
        try:
            profile = models.Profile.objects.get(user=user)
        except models.Profile.DoesNotExist:
            print("Profile does not exist, creating Profile")
            profile = models.Profile(user=user)

        return profile


class UserLoginView(LoginView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if settings.AZURE_AD:
            return HttpResponseRedirect(reverse("accounts:azure_login"))
        else:
            return super().dispatch(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        remove_user_and_token(request)
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = get_user_model()
    form_class = forms.UserAccountForm
    template_name = 'registration/user_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object.username = self.object.email
        return super().form_valid(form)


def change_password(request):
    # user_model = get_user_model()
    # print(user_model.id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def account_verified(request):
    group = Group.objects.get(name='verified')
    if group in request.user.groups.all():
        messages.error(request, 'This account has already been verified')
        return redirect('index')
    else:
        if request.method == 'POST':
            form = SetPasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!

                # the user should be added to the People object of data inventory
                # user_instance = User.objects.get(pk=user.id) #for some reason, the create() method does not want to accept the user instance
                # new_person = inventory_models.Person.objects.create(
                #     user=user_instance,
                #     full_name="{}, {}".format(user.last_name, user.first_name),
                #     organization_id=6
                # )
                user.groups.add(group)

                messages.success(request, 'Your password was successfully updated!')
                return redirect('index')
        else:
            form = SetPasswordForm(request.user)
        return render(request, 'registration/account_verified.html', {
            'form': form
        })


def resend_verification_email(request, email):
    group = Group.objects.get(name='verified')
    user = User.objects.get(email__iexact=email)
    try:
        user.groups.remove(group)
    except:
        pass
    current_site = get_current_site(request)
    mail_subject = 'Activate your Gulf Region Data Management account.'
    message = render_to_string('registration/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    from_email = 'DoNotReply@{}.com'.format(settings.WEB_APP_NAME)
    email = EmailMessage(
        mail_subject, message, to=[to_email], from_email=from_email,
    )
    if settings.DEBUG:
        email.send()
    else:
        print('not sending email since in dev mode')
        print(message)

    return HttpResponse('A verification email has been sent. Please check your inbox.')


def account_request(request):
    if request.method == 'POST':
        form = forms.AccountRequestForm(request.POST)
        if form.is_valid():
            email = emails.AccountRequestEmail(form.cleaned_data)
            # send the email object
            send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                      recipient_list=email.to_list, fail_silently=False, )
            messages.success(request, 'An email with your request has been send to the application administrator')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = forms.AccountRequestForm()
    return render(request, 'registration/account_request_form.html', {
        'form': form,
    })


def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            print(123)
            user = form.save(commit=False)
            user.username = user.email
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Gulf Region Data Management account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            from_email = 'DoNotReply@{}.com'.format(settings.WEB_APP_NAME)
            email = EmailMessage(
                mail_subject, message, to=[to_email], from_email=from_email,
            )
            if settings.DEBUG:
                email.send()
            else:
                print('not sending email since in dev mode')
                print(message)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = forms.SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        messages.success(request, 'Congrats! Your account has been successfully verified')
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('Activation link is invalid!')


# def UserResetPassword(request):
#     form = UserForgotPasswordForm(None, request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save(from_email='blah@blah.com', email_template_name='path/to/your/email_template.html')

#
class UserPassWordResetView(PasswordResetView):
    template_name = "registration/user_password_reset_form.html"
    success_message = "An email has been sent!"

    def get_success_url(self, **kwargs):
        messages.success(self.request, self.success_message)
        return reverse('index')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/user_password_reset_confirm.html"

    def get_success_url(self, **kwargs):
        messages.success(self.request,
                         "Your password has been successfully reset! Please try logging in with your new password.")
        return reverse('index')


class UserLoginRequiredView(LoginView):
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        messages.error(self.request, "You must be logged in to access this page")
        return super(UserLoginRequiredView, self).get_context_data(**kwargs)


class RequestAccessFormView(LoginRequiredMixin, FormView):
    login_url = 'accounts/login_required'
    template_name = "accounts/request_access_form_popout.html"
    form_class = forms.RequestAccessForm

    def get_initial(self):
        user = self.request.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'user_id': user.id,
        }

    def form_valid(self, form):

        context = {
            "first_name": form.cleaned_data["first_name"],
            "last_name": form.cleaned_data["last_name"],
            "email": form.cleaned_data["email"],
            "user_id": form.cleaned_data["user_id"],
            "application": form.cleaned_data["application"],
            "optional_comment": form.cleaned_data["optional_comment"],
        }
        email = emails.RequestAccessEmail(context)
        # send the email object
        if settings.DEBUG:
            send_mail(message='', subject=email.subject, html_message=email.message, from_email=email.from_email,
                      recipient_list=email.to_list, fail_silently=False, )
        else:
            print('not sending email since in dev mode')
            print(email.subject)
            print(email.message)
        messages.success(self.request,
                         message="your request has been sent to the site administrator")
        return HttpResponseRedirect(reverse('accounts:close_me'))
