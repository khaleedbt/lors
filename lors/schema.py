"""
drf-spectacular doesn't know how to introspect an ImageField nested inside
a ListField (it defaults to "array of string/uri"), which makes Swagger UI
render `uploaded_photos` as plain text inputs instead of a file picker and
breaks multipart submission. This extension tells it the real shape:
an array of binary files.
"""

from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.plumbing import build_array_type, build_basic_type
from drf_spectacular.types import OpenApiTypes


class ImageListFieldExtension(OpenApiSerializerFieldExtension):
    target_class = 'lors.serializers.ImageListField'

    def map_serializer_field(self, auto_schema, direction):
        return build_array_type(build_basic_type(OpenApiTypes.BINARY))
