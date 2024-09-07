from utils import *
import pandas as pd
import re

def get_descriptions(df,start_times,text_lines):

    descriptions = []
    end = 0
    for index, row in df.iterrows():
        start = end
        end = start_times.index(float(row['Timestamp']))
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

    return descriptions

def data_entry_from_desc(descriptions):

    entries = []
    prompt = "From the following information, return a JSON object that captures all relevant information in the form of a data entry. You must judge relevant information for yourself, however note that most information provided is relevant."
    for i,text in enumerate(descriptions):
        print(i)
        entry = query_gpt4(prompt,text)
        print(entry)
        entry_json = json.loads(find_bracket(entry))
        entries.append(entry_json)

    return entries

def save_descriptions(descriptions,output_file):
    with open(output_file, 'w') as f:
        [f.write(x+"\n") for x in descriptions]

def save_entries(entries,output_file):
    with open(output_file, 'w') as f:
        json.dump(entries, f, indent=4)


def main():
    with open("temp/last_stamps.csv", 'r') as file:
        df = pd.read_csv(file)

    with open("samples/sample0_time.txt", 'r') as file:
        transcript = file.read()

    start_times,_,text_lines = dissect_transcript(transcript.split("\n"))

    descriptions = get_descriptions(df,start_times,text_lines)
    save_descriptions(descriptions,'temp/last_descriptions.txt')

    entries = data_entry(descriptions)
    save_entries(entries,'temp/last_entry.json')

if __name__ == "__main__":
    # This ensures that if the script is executed directly (e.g., `python transcribe.py`),
    # it will run the `main()` function and process the command-line arguments.
    main()
