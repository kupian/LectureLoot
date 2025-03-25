from app.models import Notification

def notification_count(request):
    """add notification count to context"""
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, read=False).count()
        return {'notifications_count': count}
    return {'notifications_count': 0}