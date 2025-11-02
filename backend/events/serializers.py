from rest_framework import serializers
from .models import Event, EventBeneficiary

class EventBeneficiarySerializer(serializers.ModelSerializer):
    charity_name = serializers.CharField(source='charity.name', read_only=True)

    class Meta:
        model = EventBeneficiary
        fields = ('charity', 'charity_name', 'allocation_percent')

class EventListSerializer(serializers.ModelSerializer):
    organiser_name = serializers.CharField(source='organiser.username', read_only=True)
    beneficiaries = EventBeneficiarySerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            'id', 'title', 'description', 'start_datetime', 'venue',
            'base_ticket_price', 'organiser_name', 'beneficiaries'
        )
