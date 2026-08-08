import json
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Brand, CarModel, Lead, Review

# Фиксированный порядок и цвет на тип заявки (см. dataviz-справочник проекта: категориальная
# палитра назначается по сущности, не по рангу/количеству — иначе цвета "прыгали" бы при
# смене соотношения жалоб/заказов). Валидировано скриптом dataviz-skill (CVD/контраст, all-pairs).
LEAD_TYPE_ORDER = [Lead.TYPE_COMPLAINT, Lead.TYPE_MAT_ORDER, Lead.TYPE_PRODUCT_ORDER]
LEAD_TYPE_COLORS = {
    Lead.TYPE_COMPLAINT: '#2a78d6',
    Lead.TYPE_MAT_ORDER: '#eb6834',
    Lead.TYPE_PRODUCT_ORDER: '#1baf7a',
}
TREND_DAYS = 14
BREAKDOWN_DAYS = 30
RECENT_LIMIT = 10


def _leads_trend_chart():
    today = timezone.localdate()
    start = today - timedelta(days=TREND_DAYS - 1)
    counts_by_day = dict(
        Lead.objects.filter(created_at__date__gte=start)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(n=Count('id'))
        .values_list('day', 'n'),
    )
    days = [start + timedelta(days=i) for i in range(TREND_DAYS)]
    return json.dumps({
        'labels': [d.strftime('%d.%m') for d in days],
        'datasets': [{
            'label': 'Заявки',
            'data': [counts_by_day.get(d, 0) for d in days],
            'borderColor': '#2a78d6',
            'backgroundColor': '#2a78d6',
            'tension': 0.3,
            'fill': False,
            'pointRadius': 3,
        }],
    })


def _leads_by_type_chart():
    start = timezone.localdate() - timedelta(days=BREAKDOWN_DAYS - 1)
    counts_by_type = dict(
        Lead.objects.filter(created_at__date__gte=start)
        .values('lead_type')
        .annotate(n=Count('id'))
        .values_list('lead_type', 'n'),
    )
    type_labels = dict(Lead.TYPE_CHOICES)
    return json.dumps({
        'labels': [type_labels[t] for t in LEAD_TYPE_ORDER],
        'datasets': [{
            'data': [counts_by_type.get(t, 0) for t in LEAD_TYPE_ORDER],
            'backgroundColor': [LEAD_TYPE_COLORS[t] for t in LEAD_TYPE_ORDER],
        }],
    })


def _recent_leads_table():
    leads = Lead.objects.select_related('car_model__brand').order_by('-created_at')[:RECENT_LIMIT]
    rows = []
    for lead in leads:
        url = reverse('admin:lors_lead_change', args=[lead.id])
        rows.append([
            format_html('<a href="{}">{}</a>', url, lead.name),
            lead.phone,
            lead.get_lead_type_display(),
            lead.get_status_display(),
            lead.created_at.strftime('%d.%m.%Y %H:%M'),
        ])
    return {'headers': ['Имя', 'Телефон', 'Тип', 'Статус', 'Дата'], 'rows': rows}


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
    context['leads_trend_chart'] = _leads_trend_chart()
    context['leads_by_type_chart'] = _leads_by_type_chart()
    context['recent_leads_table'] = _recent_leads_table()
    return context
