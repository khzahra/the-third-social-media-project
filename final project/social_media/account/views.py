from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, auth
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import Profile, Relation
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


# Create your views here.


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            user_model = User.objects.get(username=cd['username'])
            new_profile = Profile.objects.create(user=user_model)
            new_profile.save()
            user_login = auth.authenticate(username=cd['username'], password=cd['password1'])
            auth.login(request, user_login)
            messages.success(request, 'you registered successfully', 'success')
            return redirect('account:user_settings')
        return render(request, self.template_name, {'form': form})


class UserSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)
        user = User.objects.get(username=request.user)
        return render(request, 'account/settings.html', {'user_profile': user_profile, 'user': user})

    def post(self, request):
        user_profile = Profile.objects.get(user=request.user)
        user = User.objects.get(username=request.user)
        if request.FILES.get('image') is None:
            image = user_profile.profile_image
        elif request.FILES.get('image') is not None:
            image = request.FILES.get('image')

        bio = request.POST['bio']
        age = request.POST['age']
        email = request.POST['email']
        location = request.POST['location']

        user_profile.profile_image = image
        user_profile.bio = bio
        user_profile.age = age
        user_profile.location = location
        user.email = email
        user.save()
        user_profile.save()
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'Your information is not correct.', 'warning')
            return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'See you later!', 'success')
        return redirect('account:user_login')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user_profile = Profile.objects.get(user=user)
        posts = user.posts.all()
        user_post_length = len(posts)

        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            btn_text = 'unfollow'
        else:
            btn_text = 'follow'

        user_followers = len(Relation.objects.filter(to_user=user))
        user_followings = len(Relation.objects.filter(from_user=user))


        contex = {
            'user': user,
            'user_profile': user_profile,
            'posts': posts,
            'btn_text': btn_text,
            'user_followers': user_followers,
            'user_followings': user_followings,
            'user_post_length': user_post_length,
        }
        return render(request, 'account/profile.html', contex)


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            return redirect('account:user_profile', user.id)
        else:
            new_follower = Relation.objects.create(from_user=request.user, to_user=user)
            new_follower.save()
            return redirect('account:user_profile', user.id)
