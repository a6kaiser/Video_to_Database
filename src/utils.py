import openai
import os
import json
import re

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

    with open("temp/last_openai",'w') as file:
        file.write(content)

    return content

def openai_to_find(text,case="json"):
    start_index = text.find("```"+case)+3+len(case)
    end_index = text.rfind("```")  # +1 to include the "}" character
    #print(start_index)
    #print(end_index)
    return text[start_index:end_index]

def find_bracket(text):
    start_index = text.find("{")
    end_index = text.rfind("}")+1  # +1 to include the "}" character
    #print(start_index)
    #print(end_index)
    return text[start_index:end_index]

def dissect_transcript(transcript):
    # Initialize the three lists
    start_timestamps = []
    end_timestamps = []
    text_lines = []

    # Regular expression to match the structure [start --> end] text
    pattern = r"\[(.*) - (.*)\]  (.*)"

    # Loop through each line in the content
    for line in transcript:
        match = re.match(pattern, line.strip())
        if match:
            start_timestamps.append(float(match.group(1)))  # Start timestamp
            end_timestamps.append(float(match.group(2)))    # End timestamp
            text_lines.append(match.group(3))        # Text spoken

    return start_timestamps, end_timestamps, text_lines

def convert_timestamp_to_sec(timestamps):
    ret = []

    # Regular expression to match the structure [start --> end] text
    pattern = r"(\d*)\.(\d{3})"

    # Loop through each line in the content
    for x in timestamps:
        match = re.match(pattern, x.strip())
        if match:
            time = int(match.group(1))
            time += int(match.group(2))/1000
            ret.append(time)
    return ret
