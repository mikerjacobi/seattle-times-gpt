from common import AppContext
import time
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger()

@dataclass
class SubmitPromptRequest:
    thread_id: str
    prompt: str


@dataclass
class SubmitPromptResponse:
    thread_id: str
    run_id: str
    status: str

    def as_dict(self):
      return asdict(self)

def handle_submit_prompt(
    ctx: AppContext, req: SubmitPromptRequest
) -> SubmitPromptResponse:

  # ensure a thread exists
  thread_id = req.thread_id
  if thread_id == "":
    thread = ctx.openai.beta.threads.create()
    thread_id = thread.id

  # add a message to the thread
  ctx.openai.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=req.prompt
  )

  # send the message to the assistant
  run = ctx.openai.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=ctx.assistant_id,
  )

  return SubmitPromptResponse(thread_id, run_id=run.id, status=run.status)
