from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now
import json

from appointment.models import Appointment

@csrf_exempt
def create_appointment_api(request):
    """
    Handles POST request to create an appointment.
    Expects JSON: { "full_name": "...", "phone_number": "..." }

    Returns:
    - 201 on success
    - 400 with error message on failure
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name')
            phone_number = data.get('phone_number')

            if not full_name or not phone_number:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            Appointment.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                sent_at=now()
            )
            return JsonResponse({'message': 'Appointment created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)
