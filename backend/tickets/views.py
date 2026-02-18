from .llm import classify_ticket

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate

from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "priority", "status"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]
    
    @action(detail=False, methods=["post"], url_path="classify")
    def classify(self, request):
        description = request.data.get("description")

        if not description:
            return Response(
                {"error": "Description is required"},
                status=400
            )

        result = classify_ticket(description)
        return Response(result)


    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        queryset = Ticket.objects.all()

        total_tickets = queryset.count()
        open_tickets = queryset.filter(status="open").count()

        # Average tickets per day
        daily_counts = (
            queryset
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
        )

        avg_tickets_per_day = (
            daily_counts.aggregate(avg=Avg("count"))["avg"] or 0
        )

        # Priority breakdown
        priority_breakdown = dict(
            queryset.values("priority")
            .annotate(count=Count("id"))
            .values_list("priority", "count")
        )

        # Category breakdown
        category_breakdown = dict(
            queryset.values("category")
            .annotate(count=Count("id"))
            .values_list("category", "count")
        )

        return Response({
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "avg_tickets_per_day": round(avg_tickets_per_day, 2),
            "priority_breakdown": priority_breakdown,
            "category_breakdown": category_breakdown,
        })
