from botocore.exceptions import ClientError
from pathlib import Path
import boto3
import config
import uuid

s3 = boto3.client(
    "s3",
    aws_access_key_id=config.AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.REGION
)

def upload_file(image_path: str, object_name: str = None):
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
            "url": url,
            "data": get_presigned_url(object_name, url)
        }

    except ClientError as error:
        return {
            "success": False,
            "error": str(error)
        }

def get_presigned_url(object_name: str, url: str) -> dict:
    s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": config.BUCKET_NAME,
            "Key": object_name
        },
        ExpiresIn=3600
    )
    
    return {
        "key": object_name,
        "url": url
    }

def delete_object(object_name: str):
    try:
        s3.delete_object(
            Bucket=config.BUCKET_NAME,
            Key=object_name
        )
        return {
            "success": True,
            "message": "Objeto eliminado correctamente"
        }
    except ClientError as error:
        return {
            "success": False,
            "error": str(error)
        }


try:
    object_name: str = f"uploads/{uuid.uuid1()}.jpg"

    response = upload_file(
        image_path="fotografia2.jpg",
        object_name=object_name
    )

    # response = delete_object('uploads/946c5eac-e8e9-11f1-9700-285471c579ea.jpg')

    print(response)

except Exception as err:
    print(err)