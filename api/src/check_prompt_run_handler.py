from common import AppContext, logger
from dataclasses import dataclass, asdict

@dataclass
class CheckPromptRunRequest:
    thread_id: str
    run_id: str


@dataclass
class CheckPromptRunResponse:
    status: str
    messages: list

    def as_dict(self):
      return asdict(self)

def handle_check_prompt_run(
    ctx: AppContext, req: CheckPromptRunRequest
) -> CheckPromptRunResponse:

  run = ctx.openai.beta.threads.runs.retrieve(
    thread_id=req.thread_id,
    run_id=req.run_id
  ) 
  status = run.status

  messages = []
  if status == "in_progress":
    pass # client will try again
  elif status == "completed":
    msg_resp = ctx.openai.beta.threads.messages.list(
      thread_id=req.thread_id,
      order="asc"
    )
    messages = [msg.content[0].text.value for msg in msg_resp.data]
  else:
    logger.error(f"openai returned bad status {status}. run {run}")

  return CheckPromptRunResponse(status, messages)
