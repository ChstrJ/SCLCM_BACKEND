from .models import *
from django.http import JsonResponse

def validate_user(request):
    user_profile = Profile.objects.get(user=request.user)
    allowed_users = ['counselor', 'psychometrician']

    if user_profile.role not in allowed_users:
        return JsonResponse({'error': 'Permission denied.'}, status=401)

    return;


