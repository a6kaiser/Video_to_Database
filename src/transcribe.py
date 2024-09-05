import whisper
import ffmpeg
import argparse
import os

def extract_audio(video_file, output_audio_file):
    """Extract audio from video file using ffmpeg."""
    ffmpeg.input(video_file).output(output_audio_file).run()

def transcribe_audio(audio_file, model_size="small"):
    """Transcribe audio file using Whisper model."""
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_file,verbose=True)
    return result

def transcribe_video(video_file, output_file, model_size="small"):
    """Extract audio from video and transcribe it."""
    audio_file = "temp_audio.wav"

    # Extract audio from video
    extract_audio(video_file, audio_file)

    # Transcribe audio
    transcript = transcribe_audio(audio_file, model_size=model_size)

    # Save the transcript
    with open(output_file, 'w') as f:
        for segment in transcript['segments']:
            start = segment['start']
            end = segment['end']
            text = segment['text']
            f.write(f"[{start:.2f} - {end:.2f}] {text}\n")

    # Clean up the temporary audio file
    os.remove(audio_file)

def main():
    print("starting")
    # Set up argument parser to get sample index
    parser = argparse.ArgumentParser(description="Transcribe video files using Whisper.")
    parser.add_argument("index", type=int, help="Sample index (an integer).")
    parser.add_argument("--model_size", type=str, default="small", help="Whisper model size to use.")

    print("parsing over")
    # Parse the arguments
    args = parser.parse_args()
    index = args.index
    model_size = args.model_size

    # Construct file paths, assuming the samples are in a folder named "samples"
    video_file = os.path.join("samples", f"sample{index}.mp4")
    output_file = os.path.join("samples", f"sample{index}.txt")

    # Check if the video file exists
    if not os.path.isfile(video_file):
        print(f"Error: {video_file} does not exist.")
        return

    # Transcribe the video and save the transcript
    print(f"Transcribing {video_file}...")
    transcribe_video(video_file, output_file, model_size=model_size)
    print(f"Transcription complete. Transcript saved to {output_file}.")

if __name__ == "__main__":
    # This ensures that if the script is executed directly (e.g., `python transcribe.py`),
    # it will run the `main()` function and process the command-line arguments.
    main()
