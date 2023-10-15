import json
from django.core.files.uploadedfile import InMemoryUploadedFile


class InMemoryUploadedFileEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, InMemoryUploadedFile):
            return {
                'name': obj.name,
                'size': obj.size,
                'content_type': obj.content_type,
            }
        return super().default(obj)