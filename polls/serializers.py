from rest_framework import serializers
from .models import Poll, Option, Vote

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']


class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_at', 'expires_at', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        for option in options_data:
            Option.objects.create(poll=poll, **option)
        return poll


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['poll', 'option', 'voter_id']
