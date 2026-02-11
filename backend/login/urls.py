from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path('parent/register/', views.parent_register, name="parent_register"),
    path('register/', views.register, name="register"),
    path('signout/', views.signout, name="signout"),

    path('selection/', views.selection, name="selection"),

    path('diet/plan/', views.diet_plan, name="diet_plan"),
    path('add/diet/plan/', views.add_diet_plan, name="add_diet_plan"),

    path('postnatal_care_tips/', views.postnatal_care_tips, name="postnatal_care_tips"),
    path('add_postnatal_care/', views.add_postnatal_care, name="add_postnatal_care"),

    path('fitness_exercises/', views.fitness_exercises, name="fitness_exercises"),
    path('add_fitness_exercises/', views.add_fitness_exercises, name="add_fitness_exercises"),

    path('food_recipe/', views.food_recipe, name="food_recipe"),
    path('add_food_recipe/', views.add_food_recipe, name="add_food_recipe"),

    path('vaccination/', views.vaccination, name="vaccination"),
    path('add_vaccination/', views.add_vaccination, name="add_vaccination"),
    path('book_vaccination/', views.book_vaccination, name="book_vaccination"),

    path('search/', views.search, name="search"),

    path('chat/', views.chat, name="chat"),
    path("send-group-message/", views.send_group_message, name="send_group_message"),

    path("view_pediatrician/", views.view_pediatrician, name="view_pediatrician"),
    path("view_therapist/", views.view_therapist, name="view_therapist"),

    path("profile/", views.profile, name="profile"),
    path("edit_profile/<int:id>/", views.edit_profile, name="edit_profile"),

    path("forget_password/", views.forget_password, name="forget_password"),


    path("emergency_preparedness/", views.emergency_preparedness, name="emergency_preparedness"),
    path("add_emergency_preparedness/", views.add_emergency_preparedness, name="add_emergency_preparedness"),

    path("stories/", views.stories, name="stories"),
    path("add_stories/", views.add_stories, name="add_stories"),

    path("diy_tutorial/", views.diy_tutorial, name="diy_tutorial"),
    path("add_diy_tutorial/", views.add_diy_tutorial, name="add_diy_tutorial"),

    path("checklist_view/", views.checklist_view, name="checklist_view"),
    path("add-task/", views.add_task, name="add_task"),
    path("toggle_task/<int:task_id>/", views.toggle_task, name="toggle_task"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)