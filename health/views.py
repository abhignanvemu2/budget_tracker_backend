from django.db import connection
from django.http import JsonResponse

def db_health_check(request):
    try:
        connection.ensure_connection()
        return JsonResponse({"status": "connected"})
    except Exception as e:
        return JsonResponse({"status": "error", "detail": str(e)}, status=500)
