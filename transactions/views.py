from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.utils.timezone import now
from .models import Transaction
from .serializers import TransactionSerializer
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["category", "date"]
    ordering_fields = ["amount", "date"]
    ordering = ["-date"]
    lookup_field = "id"

    def get_queryset(self):
        user_id = self.request.user.uid  # Get Firebase UID from request
        return Transaction.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.request.user.uid  # Get Firebase UID
        transaction = serializer.save(user_id=user_id)  # Save transaction with UID

        try:
            categories = ["food", "transport", "shopping", "bills", "entertainment", "health", "other", "house"]
            result = classifier(transaction.description, candidate_labels=categories)
            if "labels" in result and result["labels"]:
                transaction.category = result["labels"][0]
                transaction.save()
        except Exception as e:
            print(f"AI categorization failed: {e}")  

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        user_id = request.user.uid  
        year = request.GET.get("year", now().year)
        month = request.GET.get("month", now().month)

        transactions = Transaction.objects.filter(user_id=user_id, date__year=year, date__month=month)
        total_expense = transactions.aggregate(Sum("amount"))["amount__sum"] or 0

        category_summary = (
            transactions.values("category")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        labels = [item["category"] for item in category_summary]
        values = [float(item["total"]) for item in category_summary]

        return Response({"labels": labels, "values": values, "total_expense": total_expense})

    @action(detail=False, methods=['get'])
    def yearly_summary(self, request):
        user_id = request.user.uid  
        year = request.GET.get("year", now().year)

        transactions = Transaction.objects.filter(user_id=user_id, date__year=year)
        total_expense = transactions.aggregate(Sum("amount"))["amount__sum"] or 0

        category_summary = (
            transactions.values("category")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        labels = [item["category"] for item in category_summary]
        values = [float(item["total"]) for item in category_summary]

        return Response({"labels": labels, "values": values, "total_expense": total_expense})
    
    @action(detail=False, methods=['get'])
    def category_summary(self, request):
        user_id = request.user.uid  

        summary = (
            Transaction.objects.filter(user_id=user_id)
            .values("category")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        data = {
            "labels": [item["category"] for item in summary],
            "values": [item["total"] for item in summary],
            "total_expense": sum(item["total"] for item in summary),
        }

        return Response(data)
