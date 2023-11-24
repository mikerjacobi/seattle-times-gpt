import inspect
import json
import os
import traceback
from dataclasses import asdict
from common import AppContext, logger

import boto3
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from hello_world_handler import handle_hello_world
from submit_prompt_handler import handle_submit_prompt, SubmitPromptRequest
from check_prompt_run_handler import handle_check_prompt_run, CheckPromptRunRequest
from openai import OpenAI

cors_config = CORSConfig(allow_origin="*", allow_headers=["*"])
app = APIGatewayRestResolver(cors=cors_config)

# dynamodb = boto3.client("dynamodb")
env = os.environ["ENV"]
asst_id = os.environ["ASSISTANT_ID"]
if env == "sandbox":
    # dynamodb_url = os.environ["TP_DYNAMODB_URL"]
    # dynamodb = boto3.client("dynamodb", endpoint_url=dynamodb_url)
    pass

ctx = AppContext(
    boto3.client("s3"),
    # dynamodb,
    OpenAI(),
    env,
    assistant_id=asst_id,
)


@app.get("/hello")
def get_hello():
    func = inspect.currentframe().f_code.co_name
    try:
        resp = handle_hello_world()
        logger.warning(f"successfully handled {func}")
        return asdict(resp), 200
    except Exception as e:
        logger.error(f"failed to handle {func}. {traceback.format_exc()}")
        return {"message": "Server Error"}, 500


@app.post("/prompt")
def submit_prompt():
    func = inspect.currentframe().f_code.co_name
    try:
        request_data = json.loads(app.current_event.decoded_body)
        req = SubmitPromptRequest(**request_data)
        logger.append_keys(thread_id=req.thread_id)
        logger.info(f"received prompt: {req.prompt}")
        resp = handle_submit_prompt(ctx, req)
        logger.append_keys(run_id=resp.run_id)
        logger.info(f"success")
        return resp.as_dict(), 200
    except Exception as e:
        logger.error(f"failed to handle {func}. {traceback.format_exc()}")
        return {"message": "Server Error"}, 500

@app.get("/prompt/<thread_id>/<run_id>")
def check_prompt_run(thread_id, run_id):
    func = inspect.currentframe().f_code.co_name
    try:
        request_data = {
          "thread_id": thread_id,
          "run_id": run_id
        }
        req = CheckPromptRunRequest(**request_data)
        logger.append_keys(thread_id=req.thread_id)
        logger.append_keys(run_id=req.run_id)
        resp = handle_check_prompt_run(ctx, req)
        logger.append_keys(run_status=resp.status)
        logger.append_keys(num_messages=len(resp.messages))
        logger.info(f"successfully checked prompt run")
        return resp.as_dict(), 200
    except Exception as e:
        logger.error(f"failed to handle {func}. {traceback.format_exc()}")
        return {"message": "Server Error"}, 500


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
