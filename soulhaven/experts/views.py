from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Expert
from django.shortcuts import get_object_or_404

@csrf_exempt
def expert_detail_api(request, expert_id):
    """
    API view that returns expert detail as JSON.

    Parameters:
    - expert_id: ID of the Expert to retrieve.

    Returns:
    - JSON response with expert fields, or 404 if not found.
    """
    if request.method == 'GET':
        expert = get_object_or_404(Expert, id=expert_id)
        return JsonResponse({
            'id': expert.id,
            'name': expert.name,
            'email': expert.email,
            'platform_title': expert.platform_title,
            'specialization': expert.specialization,
            'experience': expert.experience,
            'education': expert.education,
            'methods': expert.methods,
            'tools': expert.tools,
            'certificate_text': expert.certificate_text,
            'personal_message': expert.personal_message,
            'available': expert.available,
            'created_at': expert.created_at.isoformat()
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)
