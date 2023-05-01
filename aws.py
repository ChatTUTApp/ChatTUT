import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from io import BytesIO 
from tempfile import NamedTemporaryFile 
import json 

from transformers import BertJapaneseTokenizer, AutoModelForQuestionAnswering

class AWS:
    def __init__(self):
        load_dotenv("variable.env")

        try:
            # Do not hard code credentials
            self.s3 = boto3.client(
                's3',
                region_name=os.getenv("AWS_DEFAULT_REGION"),
                # Hard coded strings as credentials, not recommended.
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
            )
            # AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
            # AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
            # AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
            # self.s3 = boto3.resource('s3')
            # self.bucket = self.s3.Bucket(os.getenv("AWS_S3_BUCKET_NAME"))
            self.bucket = "chattut"
        except ClientError as e:
            import traceback
            traceback.print_exc(e)

    # def get_model_from_s3(self):
    #     huggingface_estimator.fit({
    #         'train': 's3://<my-bucket>/<prefix>/train',  # containing train files
    #         'test': 's3://<my-bucket>/<prefix>/test',  # containing test files
    #         'model':  's3://<another-bucket>/<prefix>/model',  # containing model files (config.json, pytroch_model.bin, etc.)
    #     })
    #     return model_folder

    def s3_fileobj(self, key): 
        """
        Yields a file object from the filename at {bucket}/{key}

        Args:
            bucket (str): Name of the S3 bucket where you model is stored
            key (str): Relative path from the base of your bucket, including the filename and extension of the object to be retrieved.
        """
        obj = self.s3.get_object(Bucket=self.bucket, Key=key) 
        yield BytesIO(obj["Body"].read()) 

    def load_model(self, path_to_model, model_name='pytorch_model'):
        """
        Load a model at the given S3 path. It is assumed that your model is stored at the key:

            '{path_to_model}/{model_name}.bin'

        and that a config has also been generated at the same path named:

            f'{path_to_model}/config.json'

        """
        tempfile = NamedTemporaryFile() 
        with self.s3_fileobj(f'{path_to_model}/{model_name}.bin') as f: 
            tempfile.write(f.read()) 
    
        with self.s3_fileobj(f'{path_to_model}/config.json') as f: 
            dict_data = json.load(f) 
            # config = AutoModelForQuestionAnswering.from_pretrained(dict_data)
            config = AutoModelForQuestionAnswering.from_config(dict_data)
            # config = PretrainedConfig.from_dict(dict_data) 
    
        # model = PreTrainedModel.from_pretrained(tempfile.name, config=config) 
        return config 

if __name__ == "__main__":
    aws = AWS()
    aws.get_model_from_bucket()



