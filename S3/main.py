import boto3
import config
from pathlib import Path
from botocore.exceptions import ClientError

# Inicializar cliente S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=config.AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.REGION
)

def upload_image(image_path: str, object_name: str = None):
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {image_path}")

    if object_name is None:
        object_name = path.name

    try:
        s3.upload_file(
            str(path),
            config.BUCKET_NAME,
            object_name,
            ExtraArgs={
                "ContentType": "image/jpeg"
            }
        )

        url = f"https://{config.BUCKET_NAME}.s3.{config.REGION}.amazonaws.com/{object_name}"

        return {
            "success": True,
            "key": object_name,
            "url": url
        }

    except ClientError as error:
        return {
            "success": False,
            "error": str(error)
        }


try:
    response = upload_image(
        image_path="fotografia.jpg",
        object_name="uploads/fotografia.jpg"
    )

    # S3 Response 
    # {'success': True, 'key': 'uploads/fotografia.jpg', 'url': 'https://python-bucket-created-at-20261124.s3.us-east-1.amazonaws.com/uploads/fotografia.jpg'}

    print(response)

except Exception as err:
    print(err)