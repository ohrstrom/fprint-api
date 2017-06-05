from storages.backends.s3boto import S3BotoStorage

MediaRootS3BotoStorage  = lambda: S3BotoStorage(location='media')

# staticfiles storage is _NOT_ using s3 at the moment
StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
