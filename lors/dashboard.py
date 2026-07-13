from .models import Brand, CarModel, Complaint, Review


def dashboard_callback(request, context):
    context['kpi'] = [
        {'title': 'Марок', 'value': Brand.objects.count(), 'icon': 'directions_car'},
        {'title': 'Моделей в каталоге', 'value': CarModel.objects.count(), 'icon': 'view_list'},
        {
            'title': 'Новые жалобы',
            'value': Complaint.objects.filter(status=Complaint.STATUS_NEW).count(),
            'icon': 'report',
        },
        {
            'title': 'Отзывы на модерации',
            'value': Review.objects.filter(is_published=False).count(),
            'icon': 'rate_review',
        },
    ]
    return context
