from rest_framework import serializers
from secrets import token_hex

from secret.models import Secret
from secret.service import format_date_time


class SecretSerializer(serializers.ModelSerializer):

    class Meta:
        model = Secret
        read_only_fields = ('pk', 'owner',)
        fields = '__all__'

    def create(self, validated_data):
        days = int(validated_data.get('life_days'))
        date_of_burning = format_date_time(days)

        user = self.context['request'].user
        validated_data['owner'] = user

        secret_key = token_hex(16)
        validated_data['secret_key'] = secret_key

        secret = Secret.objects.create(
            date_of_burning=date_of_burning, **validated_data
        )
        secret.save()

        return secret
