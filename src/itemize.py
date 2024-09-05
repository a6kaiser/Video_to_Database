from utils import *
import json
import csv
import pandas as pd
from io import StringIO

def itemize(transcript):

    prompt = "For the following transcript, can you return just a CSV table of timestamps for every time that speaker transitions to a different item, and include the name of each item."
    timestamps = query_gpt4(prompt,transcript)
    #with open("last_stamps.txt", 'r') as file:
    #    timestamps = file.read()

    with open('last_stamps.txt', 'w') as f:
        f.write(timestamps)

    time_csv = openai_to_find(timestamps,'csv')
    with open('last_stamps.csv', 'w') as f:
        f.write(time_csv)

    csv_data = StringIO(time_csv)
    return pd.read_csv(csv_data)

def main():
    with open("samples/sample0_time.txt", 'r') as file:
        transcript = file.read()

    itemize(transcript)

if __name__ == "__main__":
    # This ensures that if the script is executed directly (e.g., `python transcribe.py`),
    # it will run the `main()` function and process the command-line arguments.
    main()


"""
data = eval(openai_to_find(timestamps))
with open('last_stamps.json', 'w') as f:
    json.dump(data, f, indent=4)
"""
