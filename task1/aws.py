from storages.backends.s3boto3 import S3Boto3Storage


class DefaultFileStorage(S3Boto3Storage):
    """For files and media."""

    location = "media"
    file_overwrite = False


class DefaultStaticStorage(S3Boto3Storage):
    """For static files."""

    location = "static"
