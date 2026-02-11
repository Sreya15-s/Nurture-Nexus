from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Custom user model
class User(AbstractUser):
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=15, null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
    profile = models.ImageField(upload_to="profile/")
    role = models.CharField(max_length=100, null=True, blank=True)
    specialisation = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    hospital = models.CharField(max_length=100, null=True, blank=True)

    username = None

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.fullname

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Resource_tbl(models.Model):
    category = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = 'resource_tbl'

    def __str__(self):
        return self.category
    

class ChildDiet(models.Model):
    age_months = models.CharField(max_length=250, null=True, blank=True)
    feeding_type = models.CharField(max_length=250, null=True, blank=True)
    frequency_per_day = models.CharField(max_length=250, null=True, blank=True)
    quantity_per_feed_ml = models.CharField(max_length=250, null=True, blank=True)
    Notes = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = 'child_diet_plan'

    
class PostnatalCare(models.Model):
    category = models.CharField(max_length=250, null=True, blank=True)
    tip_number = models.CharField(max_length=250, null=True, blank=True)
    Tips = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = 'postnatal_care_tips'


class Fitness(models.Model):
    exercise_name = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    instructions = models.CharField(max_length=250, null=True, blank=True)
    duration_reps = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = 'fitness_exercises'


class VaccinationSchedule(models.Model):
    age_group = models.CharField(max_length=250, null=True, blank=True)  
    vaccine_name = models.CharField(max_length=250, null=True, blank=True)  
    dose_number = models.IntegerField(null=True, blank=True)  
    description = models.TextField(null=True, blank=True)  

    class Meta:
        db_table = 'vaccination_schedule'
    
    def __str__(self):
        return f"{self.vaccine_name} - {self.age_group} (Dose {self.dose_number})"
    

class VaccinationBooking(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE) 
    child_name = models.CharField(max_length=250)  
    child_age = models.IntegerField()  
    vaccination = models.ForeignKey(VaccinationSchedule, on_delete=models.CASCADE)  
    appointment_date = models.DateField()  
    status_choices = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')  

    class Meta:
        db_table = 'vaccination_booking'
    
    def __str__(self):
        return f"Booking for {self.child_name} - {self.vaccination.vaccine_name} on {self.appointment_date}"


class ChatGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255) 
    members = models.ManyToManyField(User, related_name="chat_groups")  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, related_name="group_messages", null=True, blank=True, on_delete=models.CASCADE)  
    receiver = models.ForeignKey(User, related_name="received_messages", null=True, blank=True, on_delete=models.CASCADE) 
    message = models.TextField()
    image = models.ImageField(upload_to="chat_images/", null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        db_table = 'chat_message'
        ordering = ['timestamp']

    def __str__(self):
        if self.group:
            return f"Group Message from {self.sender} in {self.group.name} at {self.timestamp}"
        return f"Direct Message from {self.sender} to {self.receiver} at {self.timestamp}"
    

class HealthyFoodRecipe(models.Model):
    title = models.CharField(max_length=255)  
    ingredients = models.TextField()  
    instructions = models.TextField()  
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")  
    suitable_age = models.CharField(max_length=100, blank=True, null=True, help_text="Suitable age range")
    nutrition_facts = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'healthy_food_recipes'

    def __str__(self):
        return self.title




class EmergencyPreparedness(models.Model):
    Emergency_type = models.CharField(max_length=255)  
    symptoms = models.TextField()  
    immediate_action = models.TextField()   

    class Meta:
        db_table = 'emergency_preparedness'

    def __str__(self):
        return self.Emergency_type


class Stories(models.Model):
    title = models.CharField(max_length=255)  
    age_group = models.CharField(max_length=100)  
    Genre = models.CharField(max_length=100)   
    story = models.TextField()   
    moral = models.CharField(max_length=255, null=True, blank=True)   

    class Meta:
        db_table = 'stories'

    def __str__(self):
        return self.title

class DIY(models.Model):
    title = models.CharField(max_length=255)  
    video = models.FileField(upload_to="video/")  
    
    class Meta:
        db_table = 'diy'

    def __str__(self):
        return self.title
    

class ChecklistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assign tasks to users
    task = models.CharField(max_length=255)  # The to-do item
    completed = models.BooleanField(default=False)  # Status of the task
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return self.task