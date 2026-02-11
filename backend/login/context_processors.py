from datetime import date
from django.utils.timezone import now
from .models import VaccinationBooking

def vaccination_alert(request):
    if request.user.is_authenticated:
        # Get the nearest upcoming vaccination for the logged-in user
        upcoming_vaccination = VaccinationBooking.objects.filter(
            parent=request.user, 
            appointment_date__gte=date.today()
        ).order_by('appointment_date').first()

        if upcoming_vaccination:
            days_left = (upcoming_vaccination.appointment_date - date.today()).days
            return {'vaccination_alert': f"Upcoming Vaccination: {upcoming_vaccination.vaccination.vaccine_name} in {days_left} days!"}

    return {'vaccination_alert': None}
