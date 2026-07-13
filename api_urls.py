from django.urls import path
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from courses.models import Enrollment
from ebooks.models import EbookPurchase
from membership.models import UserMembership
from payments.models import Payment


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    user = request.user
    return Response({
        'enrollments': Enrollment.objects.filter(user=user).count(),
        'ebooks': EbookPurchase.objects.filter(user=user).count(),
        'membership': UserMembership.objects.filter(user=user, status='active').exists(),
        'payments': Payment.objects.filter(user=user, status='completed').count(),
    })


urlpatterns = [
    path('stats/', user_stats, name='user_stats'),
]
