import os
import boto3


class S3Api:
    _bucket_name = os.environ.get("NEWSLETTER_S3_BUCKET")
    _app_instructions_key = "app-instructions.html"
    _s3_client = boto3.client("s3")
    _s3_resource = boto3.resource("s3")

    @classmethod
    def download_html_template(cls, local_location):
        try:
            # Fetch and download css, images and fonts folder
            bucket = cls._s3_resource.Bucket(cls._bucket_name)
            for obj in bucket.objects.filter():
                # get only html files
                if obj.key.endswith("html"):
                    local_path = local_location + obj.key
                    print(f"local location: {local_location}")
                    print(f"local_path = {local_path}")
                    # save to same path
                    with open(local_path, "wb") as local_file:
                        cls._s3_client.download_fileobj(cls._bucket_name, obj.key, local_file)
        except Exception as e:
            raise RuntimeError(f"An error occurred while downloading html templates from S3: {e}")

    @classmethod
    def download_app_instructions(cls, local_location):
        try:
            # Fetch and download css, images and fonts folder
            cls._s3_resource.Bucket(cls._bucket_name).download_file(cls._app_instructions_key,
                                                                           local_location +
                                                                           cls._app_instructions_key)
        except Exception as e:
            raise RuntimeError(f"An error occurred while downloading app instructions: {e}")
