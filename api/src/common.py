from dataclasses import dataclass
import boto3
import botocore
from openai import OpenAI
from aws_lambda_powertools import Logger


@dataclass
class AppContext:
    s3: botocore.client.BaseClient
    # dynamodb: botocore.client.BaseClient
    openai: OpenAI
    env: str = "sandbox"
    assistant_id: str = ""

logger = Logger("seattle-times-gpt", level="INFO")
