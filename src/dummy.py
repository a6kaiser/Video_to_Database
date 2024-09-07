from moviepy.editor import VideoFileClip
from PIL import Image
import numpy as np

def save_first_frame(video_path, output_file):
    # Load the video file
    video = VideoFileClip(video_path)

    if video.rotation == 90:
        video = video.resize(video.size[::-1])
        video.rotation = 0

    # saving a frame at 2 second
    video.save_frame("temp/frame1.png", t = 0)

    # Get the first frame
    frame = video.get_frame(0)  # Timestamp 0 seconds for the first frame

    print("Frame shape:", frame.shape)  # Should be (height, width, 3) or (height, width)
    print("Frame dtype:", frame.dtype)  # Should be uint8

    # Convert the frame to a PIL image
    first_frame_image = Image.fromarray(np.array(frame, dtype=np.uint8))

    # Save the image
    first_frame_image.save(output_file)
    print(f"Saved first frame as {output_file}")

# Example usage
video_path = 'samples/sample1.mp4'
output_file = 'temp/first_frame.jpg'
save_first_frame(video_path, output_file)
