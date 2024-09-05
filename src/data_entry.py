from utils import *
import pandas as pd
import re

def dissect_transcript(transcript):
    # Initialize the three lists
    start_timestamps = []
    end_timestamps = []
    text_lines = []

    # Regular expression to match the structure [start --> end] text
    pattern = r"\[(.*) --> (.*)\]  (.*)"

    # Loop through each line in the content
    for line in transcript:
        match = re.match(pattern, line.strip())
        if match:
            start_timestamps.append(match.group(1))  # Start timestamp
            end_timestamps.append(match.group(2))    # End timestamp
            text_lines.append(match.group(3))        # Text spoken

    return start_timestamps, end_timestamps, text_lines

def data_entry(df,start_times,text_lines):

    descriptions = []
    end = 0
    for index, row in df.iterrows():
        start = end
        end = start_times.index(row['Timestamp'])
        if index == 0: continue
        description = ""
        #print(start,end)
        #print([text_lines[i] for i in range(start,end)])
        for i in range(start,end):
            description += text_lines[i]
        descriptions.append(description)

    description = ""
    for line in text_lines[start:]:
        description += line + " "
    descriptions.append(description)

    with open('last_descriptions.txt', 'w') as f:
        [f.write(x+"\n") for x in descriptions]

    entries = []
    prompt = "From the following information, return a JSON object that captures all relevant information in the form of a data entry. You must judge relevant information for yourself, however note that most information provided is relevant."
    for i,text in enumerate(descriptions):
        print(i)
        entry = query_gpt4(prompt,text)
        print(entry)
        entry_json = json.loads(openai_to_find(entry))
        entries.append(entry_json)

    return entries


def main():
    with open("last_stamps.csv", 'r') as file:
        df = pd.read_csv(file)

    with open("samples/sample0_time.txt", 'r') as file:
        transcript = file.read()

    start_times,_,text_lines = dissect_transcript(transcript.split("\n"))
    entries = data_entry(df,start_times,text_lines)

    with open('last_entry.json', 'w') as f:
        json.dump(entries, f, indent=4)

if __name__ == "__main__":
    # This ensures that if the script is executed directly (e.g., `python transcribe.py`),
    # it will run the `main()` function and process the command-line arguments.
    main()
