"""Armazenamento compatível com S3 e Cloudflare R2."""

import os

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class S3CompatibleStorage(Storage):
    def __init__(self):
        import boto3

        self.bucket_name = os.environ["AWS_STORAGE_BUCKET_NAME"]
        self.custom_domain = os.environ.get("AWS_S3_CUSTOM_DOMAIN", "").strip()
        self.endpoint_url = (os.environ.get("AWS_S3_ENDPOINT_URL") or "").strip()
        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name=os.environ.get("AWS_S3_REGION_NAME", "auto") or "auto",
            endpoint_url=self.endpoint_url or None,
        )

    def _save(self, name, content):
        content.seek(0)
        extra = {}
        content_type = getattr(content, "content_type", "") or ""
        if content_type:
            extra["ContentType"] = content_type
        kwargs = {"ExtraArgs": extra} if extra else {}
        self.client.upload_fileobj(content, self.bucket_name, name, **kwargs)
        return name

    def delete(self, name):
        self.client.delete_object(Bucket=self.bucket_name, Key=name)

    def exists(self, name):
        from botocore.exceptions import ClientError

        try:
            self.client.head_object(Bucket=self.bucket_name, Key=name)
            return True
        except ClientError:
            return False

    def size(self, name):
        return self.client.head_object(Bucket=self.bucket_name, Key=name)["ContentLength"]

    def url(self, name):
        if self.custom_domain:
            domain = self.custom_domain.removeprefix("https://").removeprefix("http://").strip("/")
            return f"https://{domain}/{name}"
        if self.endpoint_url:
            return f"{self.endpoint_url.rstrip('/')}/{self.bucket_name}/{name}"
        region = os.environ.get("AWS_S3_REGION_NAME", "us-east-1") or "us-east-1"
        return f"https://{self.bucket_name}.s3.{region}.amazonaws.com/{name}"
