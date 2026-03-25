from dotenv import load_dotenv
from openai import OpenAI
import json
import logging
import os
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Protected read-only profile inputs (never written by this app).
PATH_LINKEDIN_PDF = "me/linkedin.pdf"
PATH_RESUME_PDF = "me/resume.pdf"
PATH_SUMMARY_TXT = "me/summary.txt"


def push(text):
    token = os.getenv("PUSHOVER_TOKEN")
    user = os.getenv("PUSHOVER_USER")
    if not token or not user:
        return
    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={"token": token, "user": user, "message": text},
            timeout=8,
        )
    except requests.RequestException as exc:
        LOGGER.warning("Pushover notification failed: %s", exc)

def safe_load_pdf(path):
    if not os.path.exists(path):
        LOGGER.info("PDF not found: %s", path)
        return ""
    try:
        with open(path, "rb") as f:
            reader = PdfReader(f)
            return "".join(page.extract_text() for page in reader.pages if page.extract_text())
    except Exception as exc:  # pypdf can raise mixed parser exceptions
        LOGGER.warning("Failed to parse PDF %s: %s", path, exc)
        return ""

def record_user_details(email, name="Name not provided", notes="not provided"):
    if "@" not in email:
        return {"recorded": "error", "reason": "invalid_email"}
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:




    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.openai = OpenAI() if api_key else None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.name = "Amirhosein Mohaddesi"
        self.linkedin = safe_load_pdf(PATH_LINKEDIN_PDF)
        self.resume = safe_load_pdf(PATH_RESUME_PDF)
        try:
            with open(PATH_SUMMARY_TXT, "r", encoding="utf-8") as f:
                self.summary = f.read().strip()
        except OSError:
            LOGGER.warning("Summary file not found at %s", PATH_SUMMARY_TXT)
            self.summary = ""

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                arguments = {}
            LOGGER.info("Tool called: %s", tool_name)
            tool = globals().get(tool_name)
            try:
                result = tool(**arguments) if tool else {}
            except Exception as exc:
                LOGGER.warning("Tool execution failed for %s: %s", tool_name, exc)
                result = {"recorded": "error", "reason": "tool_execution_failed"}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background, LinkedIn profile which you can use to answer questions and resume which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n## Resume:\n{self.resume}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        if not self.openai:
            return (
                "This Space is running in demo mode because `OPENAI_API_KEY` is not configured. "
                "Set it in environment secrets to enable AI responses."
            )
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        iterations = 0
        while not done and iterations < 6:
            iterations += 1
            try:
                response = self.openai.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=tools,
                )
            except Exception as exc:
                LOGGER.error("OpenAI request failed: %s", exc)
                return "Sorry, I could not process that request right now. Please try again."

            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls or []
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True

        if not done:
            LOGGER.warning("Chat loop reached max tool-call iterations")
        return response.choices[0].message.content


def create_chat_interface():
    me = Me()
    return gr.ChatInterface(me.chat, type="messages")


if __name__ == "__main__":
    create_chat_interface().launch()
    