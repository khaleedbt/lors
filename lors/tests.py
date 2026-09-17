from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.files.storage import FileSystemStorage
from django.test import SimpleTestCase, override_settings
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.throttling import ScopedRateThrottle
from types import SimpleNamespace

from . import meta_capi
from .serializers import MetaEventSerializer
from .views import LeadPhotoView


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class SecurityTests(SimpleTestCase):
    def test_forwarded_prefix_does_not_reset_throttle(self):
        from django.core.cache import cache
        cache.clear()
        view = SimpleNamespace(throttle_scope='lead_create')
        results = []
        for i in range(6):
            request = SimpleNamespace(
                META={'HTTP_X_FORWARDED_FOR': f'fake-{i}, 203.0.113.9'},
                user=SimpleNamespace(is_authenticated=False),
            )
            results.append(ScopedRateThrottle().allow_request(request, view))
            self.assertEqual(meta_capi.get_client_ip(request), '203.0.113.9')
        self.assertEqual(results, [True] * 5 + [False])

    def test_purchase_and_invalid_user_are_rejected(self):
        for body in [
            {'eventName': 'Purchase', 'eventId': 'test-1234'},
            {'eventName': 'PageView', 'eventId': 'test-1234', 'user': ['bad']},
            {'eventName': 'PageView', 'eventId': 'test-1234', 'customData': {'x': 'a' * 9000}},
        ]:
            self.assertFalse(MetaEventSerializer(data=body).is_valid())
        self.assertTrue(MetaEventSerializer(data={'eventName': 'PageView', 'eventId': 'test-1234'}).is_valid())

    @override_settings(META_PIXEL_ID='test', META_ACCESS_TOKEN='test')
    def test_full_queue_drops_event(self):
        request = SimpleNamespace(META={}, COOKIES={})
        with patch.object(meta_capi, '_sender_slots') as slots, patch.object(meta_capi, '_sender') as sender:
            slots.acquire.return_value = False
            meta_capi.build_and_send(request, {'eventName': 'PageView', 'eventId': 'test-1234'})
            sender.submit.assert_not_called()

    def test_meta_rate_limit_expires(self):
        from django.core.cache import cache
        cache.clear()
        with patch('lors.meta_capi.time.time', return_value=1000):
            self.assertEqual([meta_capi.is_rate_limited('203.0.113.10') for _ in range(61)], [False] * 60 + [True])
        with patch('lors.meta_capi.time.time', return_value=1200):
            self.assertFalse(meta_capi.is_rate_limited('203.0.113.10'))

    def test_private_photo_requires_staff_and_rejects_traversal(self):
        factory = APIRequestFactory()
        view = LeadPhotoView.as_view()
        with TemporaryDirectory() as directory:
            storage = FileSystemStorage(location=directory)
            from django.core.files.base import ContentFile
            storage.save('leads/photo.png', ContentFile(b'private photo'))
            with patch('lors.views.default_storage', storage):
                response = view(factory.get('/media/leads/photo.png'), filename='photo.png')
                self.assertIn(response.status_code, (401, 403))
                request = factory.get('/media/leads/photo.png')
                force_authenticate(request, user=SimpleNamespace(is_authenticated=True, is_staff=True, pk=1))
                response = view(request, filename='photo.png')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(b''.join(response.streaming_content), b'private photo')
                response.close()
                self.assertEqual(response['Cache-Control'], 'private, no-store')
                self.assertEqual(view(request, filename='../secret').status_code, 404)

    def test_catalog_does_not_expose_internal_fields(self):
        from .serializers import CarModelSerializer
        self.assertTrue({'template_code', 'notes', 'sheet_row'}.isdisjoint(CarModelSerializer().fields))

    def test_assistant_rejects_oversized_message(self):
        from assistant.serializers import AssistantMessageRequestSerializer
        serializer = AssistantMessageRequestSerializer(data={
            'channel': 'telegram', 'external_user_id': '123', 'text': 'a' * 4097,
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('text', serializer.errors)
