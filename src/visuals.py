from moviepy.editor import VideoFileClip
import os
import pandas as pd
from utils import *
import numpy as np

def extract_frames(video_path, start_time, end_time, output_folder, num_frames=5):
    """
    Extracts frames from a video file and saves them as images.

    Args:
        video_path (str): Path to the input video file.
        start_time (float): Start time in seconds.
        end_time (float): End time in seconds.
        output_folder (str): Folder to save the extracted frames.
        num_frames (int): Number of frames to extract.
    """
    # Open the video file
    video = VideoFileClip(video_path)

    # If the video needs rotation correction, handle it
    if video.rotation == 90:
        video = video.resize(video.size[::-1])
        video.rotation = 0

    # Convert timestamps (in seconds) to time intervals
    duration = end_time - start_time
    interval = duration / num_frames if num_frames > 1 else duration

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Extract frames
    for i in range(num_frames):
        # Calculate the timestamp for the frame
        timestamp = start_time + i * interval

        # Save the frame at the timestamp
        frame_file = os.path.join(output_folder, f"frame_{i}.jpg")
        video.save_frame(frame_file, t=timestamp)

        # Print for confirmation
        print(f"Saved {frame_file}")

    # Close the video file
    video.close()

def visualize(video_path,df,output_folder):
    timestamps = [float(x) for x in df["Timestamp"]]

    # Load the video file
    clip = VideoFileClip(video_path)
    print("Video width:", clip.w)
    print("Video height:", clip.h)

    # Get the duration (in seconds)
    timestamps.append(clip.duration)

    for i, (start_time, end_time) in enumerate(zip(timestamps[:-1],timestamps[1:])):
        extract_frames(video_path, start_time, end_time, f"{output_folder}/{i}_{df['Item'].iloc[i]}")


def main():
    # Example usage
    video_path = "samples/sample0.mp4"  # Path to your MP4 file

    with open("last_stamps.csv", 'r') as file:
        df = pd.read_csv(file)

    output_folder = "frames"

    visualize(video_path,df,output_folder)

if __name__ == "__main__":
    # This ensures that if the script is executed directly (e.g., `python transcribe.py`),
    # it will run the `main()` function and process the command-line arguments.
    main()
