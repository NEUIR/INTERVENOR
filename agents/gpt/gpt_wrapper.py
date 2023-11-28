import backoff
import openai
import os
import numpy as np
os.environ["http_proxy"]="127.0.0.1:7890"
os.environ["https_proxy"]="127.0.0.1:7890"
# openai.api_key = "Put your API key here"
# openai.api_key = "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"

api_list = [
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
"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",
]
api_nums = len(api_list)
class GPTAgent():
    def __init__(self, model):
        """
        :param model: The model to use for completion.
        """
        self.model = model


    @backoff.on_exception(
        backoff.fibo,
        # https://platform.openai.com/docs/guides/error-codes/python-library-error-types
        (
            openai.error.APIError,
            openai.error.Timeout,
            openai.error.RateLimitError,
            openai.error.ServiceUnavailableError,
            openai.error.APIConnectionError,
            KeyError,
        ),
    )
    def __call__(self, user_prompt, max_tokens, temperature, stop_words):
        """
        :param user_prompt: The user requirments.
        :param max_tokens: The maximum number of tokens to generate.
        :param temperature: The sampling temperature.
        :param stop: The stop sequence or a list of stop sequences.
        :return: Return the response and the usage of the model.
        """
        api_key = api_list[np.random.randint(0, api_nums)]
        openai.api_key = api_key
        response = openai.Completion.create(engine=self.model, prompt=user_prompt, max_tokens=max_tokens, temperature=temperature,
                                 stop=stop_words)
        return response.choices[0].text, response["usage"]


