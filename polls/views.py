from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Count
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer

class PollCreateView(generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        poll = serializer.validated_data['poll']
        voter_id = serializer.validated_data['voter_id']

        if Vote.objects.filter(poll=poll, voter_id=voter_id).exists():
            return Response(
                {"detail": "You have already voted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PollResultView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()

    def retrieve(self, request, *args, **kwargs):
        poll = self.get_object()
        results = (
            Vote.objects
            .filter(poll=poll)
            .values('option__text')
            .annotate(count=Count('id'))
        )
        return Response({
            "poll": poll.question,
            "results": results
        })
