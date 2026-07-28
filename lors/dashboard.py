from .models import Brand, CarModel, Lead, Review


def dashboard_callback(request, context):
    context['kpi'] = [
        {'title': 'Марок', 'value': Brand.objects.count(), 'icon': 'directions_car'},
        {'title': 'Моделей в каталоге', 'value': CarModel.objects.count(), 'icon': 'view_list'},
        {
            'title': 'Новые жалобы',
            'value': Lead.objects.filter(lead_type=Lead.TYPE_COMPLAINT, status=Lead.STATUS_NEW).count(),
            'icon': 'report',
        },
        {
            'title': 'Новые заказы',
            'value': Lead.objects.exclude(lead_type=Lead.TYPE_COMPLAINT).filter(status=Lead.STATUS_NEW).count(),
            'icon': 'shopping_cart',
        },
        {
            'title': 'Отзывы на модерации',
            'value': Review.objects.filter(is_published=False).count(),
            'icon': 'rate_review',
        },
    ]
    return context
