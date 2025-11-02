from rest_framework.generics import ListAPIView
from .models import Event
from .serializers import EventListSerializer

class PublicEventListView(ListAPIView):
    serializer_class = EventListSerializer

    def get_queryset(self):
        return (
            Event.objects
            .filter(published=True, organiser__organiser_profile__is_verified=True)
            .select_related('organiser')
            .prefetch_related('beneficiaries__charity')
            .order_by('start_datetime')
        )
