import openai
import os
import json

# Function to query GPT-4 with a prompt and a text from file
def query_gpt4(system_prompt, user_prompt):
    # Get the API key from the environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if openai.api_key is None:
        raise ValueError("API key is missing. Set the OPENAI_API_KEY environment variable.")

    system_prompt = "You are a helpful assistant. " + system_prompt

    # OpenAI API request
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000  # Adjust based on the size of the desired response
    )

    # Checking the response status
    if response["choices"][0]["finish_reason"] == "stop":
        content = response["choices"][0]["message"]["content"]
    elif response["choices"][0]["finish_reason"] == "length":
        content = "Response was truncated due to length"
    elif response["choices"][0]["finish_reason"] == "content_filter":
        content = "Content omitted due to content filter"
    else:
        content = "API response is incomplete or still in progress"
    return content

def openai_to_find(text,case="json"):
    start_index = text.find("```"+case)+3+len(case)
    end_index = text.rfind("```")  # +1 to include the "}" character
    #print(start_index)
    #print(end_index)
    return text[start_index:end_index]
