import pyaudio
import zipfile
import os
import shutil
import pandas as pd
from hume import HumeBatchClient
from hume.models.config import LanguageConfig
client = HumeBatchClient("1EUjjQmLKHJUmNhbomdrRsuyGBZ4YjoJNBly2Vrc7n5YObA9")

    # Define paths to audio files (e.g., WAV or MP3 files)
filepaths = [
        "output.wav",
        # Add more audio file paths as needed
]

    # Configure Hume for language analysis on audio
config = LanguageConfig(
    granularity="sentence",  # Set granularity to 'sentence' for processing at the sentence level
    sentiment={},  # Enable sentiment predictions
        # Add more configurations for other emotion predictions if needed
    )

import wave

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 6
filename = "output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()




print("----------")

# Initialize HumeBatchClient with your API key

# Submit a job to process the audio files with the specified configuration
job = client.submit_job(None, [config], files=filepaths)

print(job)
print("Running...")

# Wait for the job to complete and download the predictions
details = job.await_complete()
job.download_artifacts("audio_prediction.zip")
print("Predictions downloaded to audio_prediction.zip")

# Define the path to the downloaded ZIP file and the desired output directory
zip_file_path = "audio_prediction.zip"
output_directory = "C:/Users/Ritesh Kapoor/Desktop/gradio/output"

# Extract the ZIP file
zip_file_path = "C:/Users/Ritesh Kapoor/Desktop/gradio/audio_prediction.zip"
output_directory = "C:/Users/Ritesh Kapoor/Desktop/gradio/output"

with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    # Assume the CSV file is located within a subdirectory named 'csv' in the ZIP archive
    csv_file_name = None
    for filename in zip_ref.namelist():
        if filename.endswith(".csv"):
            csv_file_name = filename
            break
    
    if csv_file_name:
        # Extract the CSV file to the desired output directory
        zip_ref.extract(csv_file_name, path=output_directory)
        print(f"CSV file extracted to: {output_directory}/{csv_file_name}")

        # Rename the extracted CSV file to a desired name (optional)
        extracted_csv_path = f"{output_directory}/{csv_file_name}"
        desired_csv_path = f"{output_directory}/language.csv"
        shutil.move(extracted_csv_path, desired_csv_path)
        print(f"CSV file moved and renamed to: {desired_csv_path}")

# Close the ZIP file
zip_ref.close()

# Delete the ZIP file after extraction
os.remove(zip_file_path)
print(f"ZIP file '{zip_file_path}' deleted.")
float_columns = list(range(9, 62))
import pandas as pd

# Load the original CSV file
data = pd.read_csv('output/language.csv')

# Define column indices to drop (0-based)
column_indices_to_drop = [0] + list(range(2, 8)) + list(range(61, 76))

# Get column labels to drop
columns_to_drop = data.columns[column_indices_to_drop]

# Drop the columns
data.drop(columns_to_drop, axis=1, inplace=True)

# Save the DataFrame to a new CSV file
data.to_csv('cleaned_language.csv', index=False)

# Read the cleaned CSV file
data = pd.read_csv('cleaned_language.csv')

# Get the keys (assuming the first column is the key)
keys = data.iloc[:, 0]

# Specify the float columns
float_columns = list(range(9, 62))

# Read the CSV file again with specified float dtype
data = pd.read_csv('cleaned_language.csv', dtype={i: float for i in float_columns})

# Get the values (excluding the first column which is assumed to be the key)
values = data.iloc[:, 2:]

# Find the top 3 columns for each row
top_3_columns = values.apply(lambda row: row.nlargest(3, keep='all').index.tolist(), axis=1)

# Combine keys with top 3 columns into a dictionary
result_dict = dict(zip(keys, top_3_columns))
print(result_dict)
