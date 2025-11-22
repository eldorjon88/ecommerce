from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

from .models import Review
from apps.products.models import Product


class ReviewListCreateView(View):
    def get(self, request):
        reviews = [
            review.to_dict()
            for review in Review.objects.all()
        ]
        return JsonResponse(reviews, safe=False)

    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        
        product = get_object_or_404(Product, pk=body.get("product"))
        rating = body.get("rating")
        comment = body.get("comment", "")

        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login required"}, status=401)

        review, created = Review.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"rating": rating, "comment": comment}
        )

        if not created:
            return JsonResponse({"error": "You already reviewed this product"}, status=400)

        return JsonResponse(review.to_dict(), status=201)


class ReviewDetailView(View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        return JsonResponse(review.to_dict())

    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk)

        if review.user != request.user:
            return JsonResponse({"error": "Permission denied"}, status=403)

        review.delete()
        return JsonResponse({"deleted": True})

