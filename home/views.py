# Importing necessary modules and models
from django.contrib.auth.decorators import login_required  # Importing decorator for login requirement
from django.contrib.auth import logout  # Importing logout function
from django.http import HttpResponseForbidden  # Importing HttpResponseForbidden for access denial
from .forms import UserProfileForm, CertificationForm, LanguageForm  # Importing forms from current directory
from services.models import Overview, Category  # Importing models from Services app
from django.shortcuts import render, redirect, get_object_or_404  # Importing necessary shortcuts
from django.core.exceptions import PermissionDenied  # Importing PermissionDenied exception
from django.contrib.auth.models import User  # Importing User model
from .models import UserProfile, Certification, Language, RatingSeller  # Importing models from current directory
from django.forms import inlineformset_factory  # Importing inlineformset_factory for formset creation
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


# View function for the introductory home page
def IntroHome(request):
    if request.user.is_authenticated:
        username = request.user.username
        return redirect('home', username)
    else:
        return render(request, 'index.html')

# View function for the user's home page
@login_required()  # Requiring login for access
def home(request, identifier):
    user = get_object_or_404(User, username=identifier)  # Getting the user object
    users = User.objects.all()
    usernames = [user.username for user in users]
    user_id = [user.id for user in users]
    user_profile = UserProfile.objects.all()
    user_service_profiles = Overview.objects.all()
    user_profile_change, created = UserProfile.objects.get_or_create(user=user)

    category = Category.objects.all()
    current_user = request.user
    if identifier == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    context = {
        'user': user,
        'user_id': user_id,
        'usernames': usernames,
        'user_profile': user_profile,
        'user_service_profiles': user_service_profiles,
        'category': category,
    }
    return render(request, 'home.html', context)

# View function for editing user profile
# @csrf_exempt
<<<<<<< HEAD
# @login_required()  # Requiring login for access
# def edit_profile(request, identifier):
#     user = get_object_or_404(User, username=identifier)  # Getting the user object
#     user_profile, created = UserProfile.objects.get_or_create(user=user)

#     # Initialize context with common values
#     current_user = request.user
#     if identifier == current_user.username:
#         pass
#     else:
#         return HttpResponseForbidden("Access Denied")

#     context = {
#         'user': user,
#         'user_profile': user_profile,
#     }

#     # Checking authorization for profile editing
#     if request.user != user:
#         raise PermissionDenied("You are not authorized to edit this profile.")

#     # Creating form instances for user profile, certifications, and languages
#     user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
#     CertificationFormSet = inlineformset_factory(UserProfile, Certification, form=CertificationForm, extra=1)
#     certification_queryset = Certification.objects.filter(user_profile=user_profile)
#     certification_formset = CertificationFormSet(request.POST or None, instance=user_profile, prefix='certifications', queryset=certification_queryset)
#     LanguageFormSet = inlineformset_factory(UserProfile, Language, form=LanguageForm, extra=1)
#     language_queryset = Language.objects.filter(user_profile=user_profile)
#     language_formset = LanguageFormSet(request.POST or None, instance=user_profile, prefix='languages', queryset=language_queryset)

#     # Handling form submission
#     username_taken = False
#     email_taken = False
#     if request.method == 'POST':
#         new_username = request.POST['username']
#         new_email = request.POST['email']

#         # Checking if new username or email is already taken
#         username_taken = User.objects.filter(username=new_username).exclude(pk=user.pk).exists()
#         email_taken = User.objects.filter(email=new_email).exclude(pk=user.pk).exists()

#         if username_taken or email_taken:
#             if username_taken:
#                 context['username_message'] = "Username is already taken. Please choose another."
#             if email_taken:
#                 context['email_message'] = "Email is already taken. Please choose another."
#         else:
#             # Saving user details if form data is valid
#             user.username = new_username
#             user.email = new_email
#             user.first_name = request.POST['first_name']
#             user.last_name = request.POST['last_name']
#             user.save()

#             if user_form.is_valid() and certification_formset.is_valid() and language_formset.is_valid():
#                 user_form.save()

#                 # Deleting marked certifications
#                 for form in certification_formset.deleted_forms:
#                     if form.cleaned_data.get('id'):
#                         form.instance.delete()

#                 # Deleting marked languages
#                 for form in language_formset.deleted_forms:
#                     if form.cleaned_data.get('id'):
#                         form.instance.delete()

#                 # Saving valid certifications
#                 for form in certification_formset:
#                     if form.is_valid() and not form.cleaned_data.get('id'):
#                         certification = form.save(commit=False)
#                         if certification.title and certification.issuing_organization:
#                             certification.user_profile = user_profile
#                             certification.save()

#                 # Saving valid languages
#                 for form in language_formset:
#                     if form.is_valid() and not form.cleaned_data.get('id'):
#                         language = form.save(commit=False)
#                         if language.language and language.proficiency:
#                             language.user_profile = user_profile
#                             language.save()

#                 # Redirecting to the user's introductory home page
#                 return redirect('IntroHome')

#     # Updating context with form instances and other necessary data
#     context.update({
#         'user_form': user_form,
#         'certification_formset': certification_formset,
#         'language_formset': language_formset,
#         'username_taken': username_taken,
#         'email_taken': email_taken,
#     })
#     return render(request, 'edit_profile.html', context)


@login_required
def edit_profile(request, identifier):
    user = get_object_or_404(User, username=identifier)
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Initialize context with common values
    current_user = request.user
    if identifier != current_user.username:
        return HttpResponseForbidden("Access Denied")

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

            certification_formset.instance = user_profile
            certification_formset.save()
            language_formset.instance = user_profile
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

<<<<<<< HEAD
    return render(request, 'edit_profile.html', context)

    user = get_object_or_404(User, username=identifier)
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Check if the current user is the profile owner
    if request.user != user:
        return HttpResponseForbidden("Access Denied")

    # Creating form instances
=======
    # Creating form instances for user profile, certifications, and languages
>>>>>>> b458055720d5929664b48f9f694cd2cf11b67e54
    user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
    CertificationFormSet = inlineformset_factory(UserProfile, Certification, form=CertificationForm, extra=1)
    certification_formset = CertificationFormSet(request.POST or None, request.FILES or None, instance=user_profile, prefix='certifications')
    LanguageFormSet = inlineformset_factory(UserProfile, Language, form=LanguageForm, extra=1)
    language_formset = LanguageFormSet(request.POST or None, request.FILES or None, instance=user_profile, prefix='languages')

    if request.method == 'POST':
<<<<<<< HEAD
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
=======
        new_username = request.POST.get('username', user.username)
        new_email = request.POST.get('email', user.email)
>>>>>>> b458055720d5929664b48f9f694cd2cf11b67e54

        # Check if new username or email is already taken
        username_taken = User.objects.filter(username=new_username).exclude(pk=user.pk).exists()
        email_taken = User.objects.filter(email=new_email).exclude(pk=user.pk).exists()

<<<<<<< HEAD
        if username_taken:
            messages.error(request, "Username is already taken.")
        elif email_taken:
            messages.error(request, "Email is already taken.")
        elif user_form.is_valid() and certification_formset.is_valid() and language_formset.is_valid():
            # Update user details
            user.username = new_username
            user.email = new_email
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()

            # Save user profile
            user_profile = user_form.save(commit=False)
            user_profile.user = user
            user_profile.save()

            # Handle profile image
            if 'profile_image' in request.FILES:
                user_profile.profile_image = request.FILES['profile_image']
                user_profile.save()

            # Save certifications and languages
            certification_formset.instance = user_profile
            certification_formset.save()
            language_formset.instance = user_profile
            language_formset.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('IntroHome')
        else:
            messages.error(request, "Please correct the errors below.")

    context = {
        'user_form': user_form,
=======
        if username_taken or email_taken:
            if username_taken:
                context['username_message'] = "Username is already taken. Please choose another."
            if email_taken:
                context['email_message'] = "Email is already taken. Please choose another."
        else:
            # Update user details if form data is valid
            user.username = new_username
            user.email = new_email
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)

            # Ensure forms are valid before saving
            if user_form.is_valid() and certification_formset.is_valid() and language_formset.is_valid():
                user.save()  # Save user only if all forms are valid
                user_form.save()

                # Deleting marked certifications and languages
                certification_formset.save()  # Handles deletes and saves
                language_formset.save()  # Handles deletes and saves

                # Redirecting to the user's introductory home page after a successful save
                return redirect('IntroHome')

    # Updating context with form instances and other necessary data
    context.update({
        'user_form': user_form, 
>>>>>>> b458055720d5929664b48f9f694cd2cf11b67e54
        'certification_formset': certification_formset,
        'language_formset': language_formset,
        'user': user,
        'user_profile': user_profile,
    }

<<<<<<< HEAD
    return render(request, 'edit_profile.html', context)
=======

>>>>>>> b458055720d5929664b48f9f694cd2cf11b67e54
# View function for viewing public profile of a user
@login_required()  # Requiring login for access
def view_profile_public(request, username):
    user = get_object_or_404(User, username=username)  # Getting the user object
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_service_profiles = Overview.objects.filter(user=user)
    seller_profile, created = UserProfile.objects.get_or_create(user=user_profile.user)
    u, created = UserProfile.objects.get_or_create(user=request.user)
    re_profile = UserProfile.objects.get(user=request.user)

    # Getting reviews for the seller profile
    profile_reviews = RatingSeller.objects.filter(seller=seller_profile)
    total_review_sum = sum(review.review_rating for review in profile_reviews)
    reviewer_profile_usr = [review.reviewer.user for review in profile_reviews]
    

    # Calculating overall rating for the seller profile
    user_profile.overall_rating = round(total_review_sum / profile_reviews.count()) if profile_reviews.count() > 0 else 0
    user_profile.save()

    # Handling form submission for adding/editing reviews
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

    # Updating context with necessary data for rendering the profile
    context = {
        'user_profile': user_profile,
        'user_service_profiles': user_service_profiles,
        'profile_reviews': profile_reviews,
        'count_review': profile_reviews.count(),
        'reviewer_profile_usr': reviewer_profile_usr,
    }

    return render(request, 'view_profile_public.html', context)