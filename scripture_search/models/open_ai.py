import os
from typing import Optional

import openai
from dotenv import load_dotenv
from smolagents.models import ChatMessage, Model

load_dotenv()


class OpenAIModel(Model):
    """A wrapper for OpenAI models that implements the Hugging Face interface."""

    def __init__(
        self, model_id: str = "gpt-4o-mini", api_key: Optional[str] = None, **kwargs
    ):
        """
        Initialize the OpenAI model wrapper.

        Args:
            model_id: The OpenAI model ID to use (e.g., "gpt-4o-mini")
            api_key: Your OpenAI API key. If None, will use OPENAI_API_KEY env var
            **kwargs: Additional arguments to pass to the OpenAI client
        """
        super().__init__(**kwargs)
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_id = model_id
        self.client = openai.OpenAI(api_key=api_key)

    def __call__(
        self,
        messages: list[dict[str, str]],
        stop_sequences: Optional[list[str]] = None,
        grammar: Optional[str] = None,
        tools_to_call_from: Optional[list[str]] = None,
        **kwargs,
    ) -> ChatMessage:
        """
        Call the OpenAI model with the given messages.

        Args:
            messages: List of message dictionaries with "role" and "content" keys
            stop_sequences: Optional list of sequences to stop generation at
            grammar: Optional grammar to constrain generation
            tools_to_call_from: Optional list of tools available to the model
            **kwargs: Additional arguments to pass to the OpenAI API

        Returns:
            A ChatMessage containing the model's response
        """
        # Convert messages to OpenAI format
        openai_messages = []
        for msg in messages:
            content = msg["content"]
            if isinstance(content, list):
                # Handle multimodal content if needed
                content = content[0]["text"] if content else ""

            openai_messages.append({"role": msg["role"], "content": content})

        # Prepare completion parameters
        completion_params = {
            "model": self.model_id,
            "messages": openai_messages,
            **kwargs,
        }

        if stop_sequences:
            completion_params["stop"] = stop_sequences

        # Call OpenAI API
        response = self.client.chat.completions.create(**completion_params)

        # Convert response to ChatMessage format
        return ChatMessage(
            role="assistant",
            content=response.choices[0].message.content,
            tool_calls=None,  # Handle tool calls if needed
        )
