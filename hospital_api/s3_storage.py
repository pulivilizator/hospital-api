from storages.backends.s3boto3 import S3Boto3Storage

from django.conf import settings


class MediaStorage(S3Boto3Storage):
    location = 'doctors'

    def url(self, name, **kwargs):
        return f'{settings.SELECTEL_CUSTOM_URL}/{self.location}/{name}'
