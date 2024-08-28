from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)  # Allows for empty values
    state = models.CharField(max_length=50, blank=True, null=True)    # Allows for empty values
    website_link = models.URLField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)  # Allows for empty values
    overall_rating = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True,
        help_text="Rating between 0.00 and 10.00"
    )
    skills = models.ManyToManyField('Skill', related_name='user_profiles', blank=True)

    def __str__(self):
        return self.user.username

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Certification(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='certifications'
    )
    title = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()

    def __str__(self):
        return f"{self.title} from {self.issuing_organization} (Issued on {self.issue_date})"
class Language(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='languages'
    )
    language = models.CharField(
        max_length=50, help_text="Name of the language"
    )
    PROFICIENCY_CHOICES = [
        ('novice', 'Novice'),
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('proficient', 'Proficient'),
    ]
    proficiency = models.CharField(
        max_length=12, choices=PROFICIENCY_CHOICES, help_text="Level of proficiency"
    )

    def __str__(self):
        return f"{self.language} - {self.get_proficiency_display()}"
class RatingSeller(models.Model):
    review_rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_given')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_received')
    title = models.CharField(max_length=50)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['seller', 'reviewer']


    



