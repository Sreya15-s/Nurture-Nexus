from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
import pycurl

# Create your views here.

def sends_mail(mail, msg):
    crl = pycurl.Curl()
    crl.setopt(crl.URL, 'https://alc-training.in/gateway.php')
    data = {'email': mail, 'msg': msg}
    pf = urlencode(data)
    crl.setopt(crl.POSTFIELDS, pf)
    crl.perform()
    crl.close()


def home(request):
    return render(request, 'index.html')


def parent_register(request):
    if request.method == "POST":
        profile = request.FILES.get('profile')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        re_pass = request.POST.get('password')

        if password != re_pass:
            messages.error(request, "Passwords do not match.")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("register")
        
        role = "parent"
        
        user = User.objects.create(profile=profile, fullname=name, email=email, phone=phone, role=role, password=password)
        user.save()
        messages.success(request, "Parent successfully registered.")
        return redirect('login')
    return render(request, 'parent_register.html')


def register(request):
    if request.method == "POST":
        profile = request.FILES.get('profile')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        specialisation = request.POST.get('specialisation')
        state = request.POST.get('state')
        district = request.POST.get('district')
        hospital = request.POST.get('hospital')
        password = request.POST.get('password')
        re_pass = request.POST.get('password')

        if password != re_pass:
            messages.error(request, "Passwords do not match.")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("register")
        
        role = request.GET.get('role')  
        
        user = User.objects.create(profile=profile,fullname=name,email=email,phone=phone,role=role,specialisation=specialisation,
                                    state=state,district=district,hospital=hospital,password=password)
        user.save()
        messages.success(request, "You have been registered successfully.")
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with this email and password exists
        user = User.objects.filter(email=email).first()  

        if user:
            if user.is_superuser:  # Check if the user is an admin
                if check_password(password, user.password):  # Validate hashed password
                    login(request, user)
                    messages.success(request, "Admin login successful.")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid admin password.")
            else:  # For non-admin users, check plain-text password
                if user.password == password and user.role == "parent":
                    login(request, user)
                    messages.success(request, "Login Successful.")
                    return redirect('selection')
                elif user.password == password:
                    login(request, user)
                    messages.success(request, "Login Successful")
                    return redirect('home')
                    
                else:
                    messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "User does not exist.")
    return render(request, 'login.html')


@login_required
def signout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def selection(request):
    return render(request, 'selection.html')


def diet_plan(request):
    result = ChildDiet.objects.all()
    print("dddddddddddddd",result)
    return render(request, 'diet_plan.html', {'result':result})


def add_diet_plan(request):
    if request.method == "POST":
        age_months = request.POST.get('age_months')
        feeding_type = request.POST.get('feeding')
        frequency_per_day = request.POST.get('frequency')
        quantity_per_feed_ml = request.POST.get('quantity')
        Notes = request.POST.get('notes')

        result = ChildDiet.objects.create(age_months=age_months,feeding_type=feeding_type,frequency_per_day=frequency_per_day,
                                          quantity_per_feed_ml=quantity_per_feed_ml,Notes=Notes)
        result.save()
        messages.success(request, "Successfully added Diet Plan")
        return redirect('diet_plan')

    return render(request, 'add_diet_plan.html')


def postnatal_care_tips(request):
    result = PostnatalCare.objects.all()
    return render(request, 'postnatal_care.html', {'result': result})


def add_postnatal_care(request):
    if request.method == "POST":
        category = request.POST.get('category')
        tip_number = request.POST.get('tip_number')
        tips = request.POST.get('tips')

        result = PostnatalCare.objects.create(category=category,tip_number=tip_number,Tips=tips)
        result.save()
        messages.success(request, "Successfully added Postnatal Care Tips")
        return redirect('postnatal_care_tips')

    return render(request, 'add_postnatal_care.html')


def fitness_exercises(request):
    result = Fitness.objects.all()
    return render(request, 'fitness.html', {'result': result})


def add_fitness_exercises(request):
    if request.method == "POST":
        exercise_name = request.POST.get('exercise_name')
        description = request.POST.get('description')
        instructions = request.POST.get('instructions')
        duration_reps = request.POST.get('duration_reps')

        result = Fitness.objects.create(exercise_name=exercise_name,description=description,instructions=instructions,duration_reps=duration_reps)
        result.save()
        messages.success(request, "Successfully added Fitness Exercises.")
        return redirect('fitness_exercises')

    return render(request, 'add_fitness.html')


def food_recipe(request):
    result = HealthyFoodRecipe.objects.all()
    return render(request, 'food_recipe.html', {'result': result})


def add_food_recipe(request):
    if request.method == "POST":
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        preparation_time = request.POST.get('preparation_time')
        suitable_age = request.POST.get('suitable_age')
        nutrition_facts = request.POST.get('nutrition_facts')
        result = HealthyFoodRecipe.objects.create(title=title,ingredients=ingredients,instructions=instructions,
                                                  preparation_time=preparation_time,suitable_age=suitable_age,nutrition_facts=nutrition_facts)
        result.save()
        messages.success(request, "Successfully added Food Recipes.")
        return redirect('food_recipe')
    return render(request, 'add_food_recipe.html')


def vaccination(request):
    result = VaccinationSchedule.objects.all()
    return render(request, 'vaccination.html', {'result': result})


def add_vaccination(request):
    if request.method == "POST":
        age_group = request.POST.get('age_group')
        vaccine_name = request.POST.get('vaccine_name')
        dose_number = request.POST.get('dose_number')
        description = request.POST.get('description')

        result = VaccinationSchedule.objects.create(age_group=age_group,vaccine_name=vaccine_name,dose_number=dose_number,description=description)
        result.save()
        messages.success(request, "Successfully added Vaccination Schedule.")
        return redirect('vaccination')

    return render(request, 'add_vaccination.html')


def book_vaccination(request):
    vaccination = VaccinationSchedule.objects.all()
    if request.method == "POST":
        child_name = request.POST.get('child_name')
        child_age = request.POST.get('child_age')
        vaccination_id = request.POST.get('vaccination')
        appointment_date = request.POST.get('appointment_date')

        vaccination = VaccinationSchedule.objects.get(id=vaccination_id)
        parent = request.user

        result = VaccinationBooking.objects.create(parent=parent,child_name=child_name,child_age=child_age,vaccination=vaccination,appointment_date=appointment_date,status="Confirmed")
        result.save()
        messages.success(request, "Vaccination Successfully Booked")
        return redirect('vaccination')
    return render(request, "book_vaccination.html", {'vaccination': vaccination})


def search(request):
    return render(request, 'search.html')


# Create a global chat group if it doesn't exist
def get_or_create_global_chat():
    group, created = ChatGroup.objects.get_or_create(name="Global Chat")
    if created:
        # Add all users to the global chat
        group.members.set(User.objects.all())  # Ensuring all users are members
    return group


# View to show the group chat messages
@login_required
def chat(request):
    role = getattr(request.user, "role", None)  # Get role if it exists

    if role in ["Therapist", "Pediatrician"]:
        template_name = "index.html"
    elif role == "parent":
        template_name = "base2.html"
    else:
        template_name = "default.html"
    group = get_or_create_global_chat()  # Get or create the global chat group
    messages = ChatMessage.objects.filter(group=group).order_by("timestamp")  # Fetch all messages
    
    return render(request, "chat.html", {"group": group, "messages": messages, "template_name": template_name})


# API to send a new message in the group chat
@csrf_exempt
@login_required
def send_group_message(request):
    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()

        if not message_text:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        group = get_or_create_global_chat()
        message = ChatMessage.objects.create(
            sender=request.user,
            group=group,
            message=message_text,
            timestamp=now(),
        )
        print(f"Group Message from2 {message.sender.fullname} in {message.group.name} at {message.timestamp}")

        return JsonResponse({"message": "Message sent", "sender": request.user.fullname, "text": message.message, "timestamp": message.timestamp})
    
    return JsonResponse({"error": "Invalid request"}, status=400)


def view_pediatrician(request):
    result = User.objects.filter(role="Pediatrician")
    return render(request, 'view_pediatrician.html', {"result": result})


def view_therapist(request):
    result = User.objects.filter(role="Therapist")
    return render(request, 'view_therapist.html', {"result": result})


def profile(request):
    profile = request.user
    return render(request, 'profile.html', {'profile':profile})


def edit_profile(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        profile_image = request.FILES.get('profile')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        specialisation = request.POST.get('specialisation')
        state = request.POST.get('state')
        district = request.POST.get('district')
        hospital = request.POST.get('hospital')
        password = request.POST.get('password')

        # Check if the email already exists but exclude the current user
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "Email is already registered with another account.")
            return redirect("edit_profile", id=user.id)

        # Only update fields if a new value is provided
        if profile_image:
            user.profile = profile_image
        user.fullname = name  
        user.email = email
        user.phone = phone
        user.specialisation = specialisation
        user.state = state
        user.district = district
        user.hospital = hospital

        if password:
            user.password

        user.save()
        messages.success(request, 'Profile Updated Successfully.')
        return redirect('profile')
    return render(request, 'edit_profile.html', {'user': user})


def forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)  # Check if email exists
            password = user.password 
            print("fffffff", password)
            sends_mail(email, f"Your Password is {password}")
            messages.info(request, "Forget password has send to your mail.")
            return redirect('login')
        except User.DoesNotExist:
            return render(request, "forget_password.html", {"error": "Email not found."})

    return render(request, 'forget_password.html')








def emergency_preparedness(request):
    result = EmergencyPreparedness.objects.all()
    return render(request, 'emergency.html', {'result': result})


def add_emergency_preparedness(request):
    if request.method == "POST":
        Emergency_type = request.POST.get('Emergency_type')
        symptoms = request.POST.get('symptoms')
        immediate_action = request.POST.get('immediate_action')
        
        result = EmergencyPreparedness.objects.create(Emergency_type=Emergency_type,symptoms=symptoms,immediate_action=immediate_action)
        result.save()
        messages.success(request, "Successfully added Emergency Preparedness.")
        return redirect('emergency_preparedness')
    return render(request, 'add_emergency.html')


def stories(request):
    result = Stories.objects.all()
    return render(request, 'stories.html', {'result': result})


def add_stories(request):
    if request.method == "POST":
        title = request.POST.get('title')
        age_group = request.POST.get('age_group')
        genre = request.POST.get('genre')
        moral = request.POST.get('moral')
        story = request.POST.get('story')
        
        result = Stories.objects.create(title=title,age_group=age_group,Genre=genre,moral=moral,story=story)
        result.save()
        messages.success(request, "Successfully added Stories.")
        return redirect('stories')
    return render(request, 'add_stories.html')


def diy_tutorial(request):
    result = DIY.objects.all()
    return render(request, 'tutorials.html', {'result': result})


def add_diy_tutorial(request):
    if request.method == "POST":
        title = request.POST.get('title')
        video = request.FILES.get('video')
        
        result = DIY.objects.create(title=title,video=video)
        result.save()
        messages.success(request, "Successfully added Stories.")
        return redirect('diy_tutorial')
    return render(request, 'add_tutorial.html')


def checklist_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX Request
        tasks = ChecklistItem.objects.filter(user=request.user, completed=False).order_by('-created_at')
        task_data = [{"id": task.id, "task": task.task, "completed": task.completed} for task in tasks]
        return JsonResponse({"tasks": task_data})
    
    # Default behavior if not an AJAX request
    tasks = ChecklistItem.objects.filter(user=request.user, completed=False).order_by('-created_at')
    return render(request, 'checklist.html', {'tasks': tasks})



def add_task(request):
    if request.method == "POST":
        task_text = request.POST.get("task")
        if task_text:
            ChecklistItem.objects.create(user=request.user, task=task_text)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


def toggle_task(request, task_id):
    try:
        task = ChecklistItem.objects.get(id=task_id, user=request.user)
        task.completed = request.POST.get("completed") == "true"  # Convert string to boolean
        task.save()
        return JsonResponse({"status": "success", "completed": task.completed})
    except ChecklistItem.DoesNotExist:
        return JsonResponse({"status": "error"}, status=404)
