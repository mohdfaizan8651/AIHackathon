from langchain.llms.base import LLM
from typing import Optional, List
import requests
import json
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory


class ClaudeSonnetLLM(LLM):
    def __init__(self, api_key: str, url: str, temperature: float = 0.7, max_tokens: int = 500):
        super().__init__()
        self._api_key = api_key
        self._url = url
        self._temperature = temperature
        self._max_tokens = max_tokens

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
      payload = {
          "api_key": self._api_key,
          "prompt": prompt,
          "model_id": "claude-3.5-sonnet",
          "model_params": {
              "max_tokens": self._max_tokens,
              "temperature": self._temperature
          }
      }

      headers = {"Content-Type": "application/json"}
      response = requests.post(self._url, headers=headers, data=json.dumps(payload))

      try:
          result = response.json()
          # FIX: Make sure we extract only the plain string
          if isinstance(result, dict) and "response" in result:
              return result # <- return only the string, not the full dict
          else:
              return "[Invalid response format]"
      except Exception as e:
          return f"[Error parsing response: {str(e)}]"


    @property
    def _llm_type(self) -> str:
        return "claude_sonnet"

    @property
    def _identifying_params(self):
        return {
            "url": self._url,
            "temperature": self._temperature,
            "max_tokens": self._max_tokens
        }
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

API_KEY = "syn-7f22e2ef-6003-4f20-9fff-23aa8729c29c"

# Initialize custom Claude model
llm = ClaudeSonnetLLM(
    api_key=API_KEY,
    url="https://quchnti6xu7yzw7hfzt5yjqtvi0kafsq.lambda-url.eu-central-1.on.aws/",
    temperature=0.7,
    max_tokens=500
)