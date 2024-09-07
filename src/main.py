from data_entry import *
from itemize import *
from transcribe import *
from utils import *
from visuals import *
import argparse
import time

def main():
    # Set up argument parser to get sample index
    parser = argparse.ArgumentParser(description="Transcribe video files using Whisper.")
    parser.add_argument("index", type=int, help="Sample index (an integer).")
    parser.add_argument("--model_size", type=str, default="small", help="Whisper model size to use.")
    parser.add_argument("--backup", type=int, default=1, help="Should you backup")

    # Parse the arguments
    args = parser.parse_args()
    index = args.index
    model_size = args.model_size
    backup = args.backup

    # Construct file paths, assuming the samples are in a folder named "samples"
    video_file = os.path.join("samples", f"sample{index}.mp4")

    output_dir = f"outputs/sample{index}"
    out_trans = os.path.join(output_dir, f"sample{index}_transcript.txt")
    out_item = os.path.join(output_dir, f"sample{index}_items.txt")
    out_desc = os.path.join(output_dir, f"sample{index}_desc.txt")
    out_entry = os.path.join(output_dir, f"sample{index}_entry.txt")
    out_vis = os.path.join(output_dir, f"sample{index}_vis.txt")

    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Check if the video file exists
    if not os.path.isfile(video_file):
        print(f"Error: {video_file} does not exist.")
        return

    # Start the overall process timer
    start_time = time.time()

    # Transcribe the video and save the transcript
    print(f"Transcribing {video_file}...")
    transcribe_start_time = time.time()
    transcript = transcribe_video(video_file, model_size=model_size)
    transcribe_end_time = time.time()
    print(f"Transcription complete. Time taken: {transcribe_end_time - transcribe_start_time:.2f} seconds.")

    if backup:
        save_transcript(transcript, out_trans)
        print(f"Transcript saved to {out_trans}.")

    # Itemizing the transcript
    print(f"Itemizing {video_file}...")
    itemize_start_time = time.time()
    df = itemize(transcript)
    itemize_end_time = time.time()
    print(f"Itemizing complete. Time taken: {itemize_end_time - itemize_start_time:.2f} seconds.")

    if backup:
        save_stamps(df, out_item)
        print(f"List saved to {out_item}.")

    # Creating the data entries
    print(f"Entering data from {video_file}...")
    data_entry_start_time = time.time()
    start_times, _, text_lines = dissect_transcript(transcript.split("\n"))
    print(start_times)
    descriptions = get_descriptions(df, start_times, text_lines)
    entries = data_entry_from_desc(descriptions)
    if backup:
        save_descriptions(descriptions, out_desc)
    save_entries(entries, out_entry)
    data_entry_end_time = time.time()
    print(f"Data entry complete. Time taken: {data_entry_end_time - data_entry_start_time:.2f} seconds.")
    print(f"Data saved to {out_entry}.")

    # Storing images from the video
    print(f"Storing images from {video_file}...")
    visualize_start_time = time.time()
    visualize(video_file, df, out_vis)
    visualize_end_time = time.time()
    print(f"Complete. Images saved to {out_vis}. Time taken: {visualize_end_time - visualize_start_time:.2f} seconds.")

    # End the overall process timer
    end_time = time.time()
    print(f"Total time for all operations: {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    # This ensures that if the script is executed directly (e.g., `python transcribe.py`),
    # it will run the `main()` function and process the command-line arguments.
    main()
