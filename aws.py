import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from io import BytesIO 

class AWS:
    def __init__(self):
        load_dotenv("variable.env")

        try:
            # Do not hard code credentials
            self.client = boto3.client(
                's3',
                region_name=os.getenv("AWS_DEFAULT_REGION"),
                # Hard coded strings as credentials, not recommended.
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
            )
            self.s3 = boto3.resource('s3')
            self.bucket = self.s3.Bucket(os.getenv("AWS_S3_BUCKET_NAME"))
        except ClientError as e:
            import traceback
            traceback.print_exc(e)

    def get_model_from_bucket(self):
        # model_folder = [obj_summary.key for obj_summary in self.bucket.objects.all()]
        file_name = "output/pytorch_model.bin"
        model_folder = self.s3.list_objects(Bucket=os.getenv("AWS_S3_BUCKET_NAME"), Prefix=file_name)
        # print(model_folder)
        # return model_folder
        return model_folder

    def s3_fileobj(self):
        file_name = "output/config.json"
        obj = self.s3.get_object(Bucket=os.getenv("AWS_S3_BUCKET_NAME"), Key=file_name) 
        # yield BytesIO(obj["Body"].read())
        return obj["Body"]

if __name__ == "__main__":
    aws = AWS()
    aws.get_model_from_bucket()



