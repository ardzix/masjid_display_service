"""
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: storage.py
# Project: core.ayopeduli.id
# File Created: Wednesday, 31st October 2018 7:26:00 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 31st October 2018 7:26:01 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Peduli sesama, sejahtera bersama
# Copyright - 2018 Ayopeduli.Id, ayopeduli.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""


from django.conf import settings
from django.core.files.storage import FileSystemStorage, DefaultStorage
from storages.backends.s3boto3 import S3Boto3Storage


USE_S3 = getattr(settings, "USE_S3", False)
USE_DO_SPACE = getattr(settings, "USE_DO_SPACE", False)  # use S3 credentials
USE_GCS = getattr(settings, "USE_GCS", False)
USE_RACKSPACE = getattr(settings, "USE_RACKSPACE", False)
GCS_BASE_URL = getattr(settings, "GCS_BASE_URL", "")
RACKSPACE_BASE_URL = getattr(settings, "RACKSPACE_BASE_URL", "")

# for DO bucket location
USE_DEFAULT_LOCATION = getattr(settings, "USE_DEFAULT_LOCATION", False)
DO_SPACE_LOCATION = getattr(settings, "DO_SPACE_LOCATION", False)

CHUNK_UPLOAD_ROOT = getattr(
    settings, "CHUNK_UPLOAD_FOLDER", "/srv/media/chunked/upload/"
)
CHUNK_UPLOAD_FINISHED_ROOT = getattr(
    settings, "CHUNK_UPLOAD_FOLDER", "/srv/media/chunked/final/"
)


def get_bucket_location(storage_type):
    if USE_DEFAULT_LOCATION and DO_SPACE_LOCATION:
        return ROOT_URL + storage_type

    return ROOT_URL


if settings.PRODUCTION:
    ROOT_URL = ""
    MEDIA_ROOT = settings.MEDIA_ROOT
    UPLOAD_ROOT = "%supload/" % settings.BASE_URL
else:
    ROOT_URL = "dev/"
    MEDIA_ROOT = settings.MEDIA_ROOT
    UPLOAD_ROOT = "%sstatic/upload/" % settings.BASE_URL

if USE_DO_SPACE and DO_SPACE_LOCATION:
    ROOT_URL = DO_SPACE_LOCATION

if USE_S3 or USE_DO_SPACE:
    VIDEO_STORAGE = S3Boto3Storage(
        location=get_bucket_location("video"), file_overwrite=False
    )
    FILE_STORAGE = S3Boto3Storage(
        location=get_bucket_location("file"), file_overwrite=False
    )
    AVATAR_STORAGE = S3Boto3Storage(
        location=get_bucket_location("picture/avatar"), file_overwrite=False
    )
    COVER_STORAGE = S3Boto3Storage(
        location=get_bucket_location("picture/cover"), file_overwrite=False
    )
    LOGO_STORAGE = S3Boto3Storage(
        location=get_bucket_location("picture/logo"), file_overwrite=False
    )
    PICTURE_STORAGE = S3Boto3Storage(
        location=get_bucket_location("picture/others"), file_overwrite=False
    )

else:
    VIDEO_STORAGE = FileSystemStorage(
        location="%s/video" % MEDIA_ROOT, base_url="%svideo/" % UPLOAD_ROOT
    )
    FILE_STORAGE = FileSystemStorage(
        location="%s/file" % MEDIA_ROOT, base_url="%sfile/" % UPLOAD_ROOT
    )
    AVATAR_STORAGE = FileSystemStorage(
        location="%s/picture/avatar" % MEDIA_ROOT,
        base_url="%spicture/avatar/" % UPLOAD_ROOT,
    )
    COVER_STORAGE = FileSystemStorage(
        location="%s/picture/cover" % MEDIA_ROOT,
        base_url="%spicture/cover/" % UPLOAD_ROOT,
    )
    LOGO_STORAGE = FileSystemStorage(
        location="%s/picture/logo" % MEDIA_ROOT,
        base_url="%spicture/logo/" % UPLOAD_ROOT,
    )
    PICTURE_STORAGE = FileSystemStorage(
        location="%s/picture/others" % MEDIA_ROOT,
        base_url="%spicture/others/" % UPLOAD_ROOT,
    )


# chunk upload storage
STORAGE_CHUNK = FileSystemStorage(
    location=settings.MEDIA_ROOT + "/chunk",
    base_url="%sstatic/upload/chunk/" % settings.BASE_URL,
)

CHUNK_UPLOAD_PRIVATE = FileSystemStorage(location=CHUNK_UPLOAD_FINISHED_ROOT)
