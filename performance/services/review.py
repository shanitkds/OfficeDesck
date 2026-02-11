from teamlead.models import TeamLeadReview

def calculate_team_lead_review(employee, month, year):

    review = TeamLeadReview.objects.filter(
        employee=employee,
        review_month__month=month,
        review_month__year=year
    ).first()

    # If no review given
    if not review:
        return {
            "rating": None,
            "review_score": 0
        }

    review_score = (review.rating / 5) * 20

    return {
        "rating": review.rating,
        "review_score": round(review_score, 2)
    }