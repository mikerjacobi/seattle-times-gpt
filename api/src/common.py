from dataclasses import dataclass
import json
import boto3
import botocore
from openai import OpenAI
from aws_lambda_powertools import Logger


@dataclass
class AppContext:
    s3: botocore.client.BaseClient
    openai: OpenAI
    env: str = "sandbox"
    assistant_id: str = ""

    def __post_init__(self):
        session = boto3.session.Session()
        secret_name = "seattle-times-gpt/prod/openai"
        client = session.client(
            service_name='secretsmanager',
            region_name="us-east-1"
        )
        resp = client.get_secret_value(SecretId=secret_name)
        api_key = json.loads(resp['SecretString'])["api_key"]
        self.openai = OpenAI(api_key=api_key)

logger = Logger("seattle-times-gpt", level="INFO")
