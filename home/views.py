# Importing necessary modules and models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.contrib import messages

from .forms import UserProfileForm, CertificationForm, LanguageForm
from .models import UserProfile, Certification, Language, RatingSeller
from services.models import Overview, Category

# View function for the introductory home page
def IntroHome(request):
    if request.user.is_authenticated:
        return redirect('home', identifier=request.user.username)
    return render(request, 'index.html')

# View function for the user's home page
@login_required
def home(request, identifier):
    user = get_object_or_404(User, username=identifier)

    if identifier != request.user.username:
        return HttpResponseForbidden("Access Denied")

    context = {
        'user': user,
        'user_id': [user.id for user in User.objects.all()],
        'usernames': [user.username for user in User.objects.all()],
        'user_profile': UserProfile.objects.all(),
        'user_service_profiles': Overview.objects.all(),
        'category': Category.objects.all(),
    }
    return render(request, 'home.html', context)

# View function for editing user profile
@login_required
def edit_profile(request, identifier):
    user = get_object_or_404(User, username=identifier)

    if identifier != request.user.username:
        return HttpResponseForbidden("Access Denied")

    user_profile, _ = UserProfile.objects.get_or_create(user=user)

    user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
    CertificationFormSet = inlineformset_factory(UserProfile, Certification, form=CertificationForm, extra=1)
    certification_formset = CertificationFormSet(request.POST or None, request.FILES or None, instance=user_profile, prefix='certifications')
    LanguageFormSet = inlineformset_factory(UserProfile, Language, form=LanguageForm, extra=1)
    language_formset = LanguageFormSet(request.POST or None, request.FILES or None, instance=user_profile, prefix='languages')

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        username_taken = User.objects.filter(username=new_username).exclude(pk=user.pk).exists()
        email_taken = User.objects.filter(email=new_email).exclude(pk=user.pk).exists()

        if username_taken:
            messages.error(request, "Username is already taken.")
        elif email_taken:
            messages.error(request, "Email is already taken.")
        elif user_form.is_valid() and certification_formset.is_valid() and language_formset.is_valid():
            user.username = new_username
            user.email = new_email
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()

            user_profile = user_form.save(commit=False)
            user_profile.user = user
            if request.FILES.get('profile_image'):
                user_profile.profile_image = request.FILES['profile_image']
            user_profile.save()

            certification_formset.save()
            language_formset.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('home', identifier=user.username)
        else:
            messages.error(request, "Please correct the errors below.")

    context = {
        'user_form': user_form,
        'certification_formset': certification_formset,
        'language_formset': language_formset,
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'edit_profile.html', context)

# View function for viewing public profile of a user
@login_required
def view_profile_public(request, username):
    user = get_object_or_404(User, username=username)
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    seller_profile, _ = UserProfile.objects.get_or_create(user=user_profile.user)
    re_profile = UserProfile.objects.get(user=request.user)

    profile_reviews = RatingSeller.objects.filter(seller=seller_profile)
    user_profile.overall_rating = round(sum(review.review_rating for review in profile_reviews) / profile_reviews.count()) if profile_reviews.count() > 0 else 0
    user_profile.save()

    if request.method == 'POST':
        rating_value = request.POST.get('rg1')
        title = request.POST.get('review_title')
        review_text = request.POST.get('review_message')
        existing_review = RatingSeller.objects.filter(seller=seller_profile, reviewer=re_profile).first()

        if existing_review:
            existing_review.review_rating = rating_value
            existing_review.title = title
            existing_review.review = review_text
            existing_review.save()
        else:
            RatingSeller.objects.create(
                seller=seller_profile,
                reviewer=re_profile,
                review_rating=rating_value,
                title=title,
                review=review_text
            )

    context = {
        'user_profile': user_profile,
        'user_service_profiles': Overview.objects.filter(user=user),
        'profile_reviews': profile_reviews,
        'count_review': profile_reviews.count(),
        'reviewer_profile_usr': [review.reviewer.user for review in profile_reviews],
    }

    return render(request, 'view_profile_public.html', context)
