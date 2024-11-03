import os
<<<<<<< HEAD
import numpy as np
import librosa
from scipy.io.wavfile import write as wav_write

def split_audio_by_lowest_energy(file_path, output_dir, large_segment_duration=720, min_length=10, max_length=15):
    """
    Splits an audio file into smaller segments without loading the entire audio into memory at once.
    First, divides the file into 5 parts based on duration, then within each part, finds the lowest
    energy point within 10 to 15 seconds to split further.
    """
    print(f"Processing file: {file_path}")
    
    # Get audio duration without loading the entire file
    duration = librosa.get_duration(path=file_path)
    print(f"Total duration (in seconds): {duration}")
    
    # Divide into 5 equal parts (or as close as possible)
    num_parts = 5
    part_duration = duration / num_parts

    # Use a short output directory path to avoid Windows path length issues
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    segment_count = 0

    # Process each part independently
    for part in range(num_parts):
        large_segment_start = part * part_duration
        large_segment_end = min((part + 1) * part_duration, duration)
        
        print(f"\nProcessing large segment from {large_segment_start:.2f}s to {large_segment_end:.2f}s")
        
        large_segment_audio, sr = librosa.load(file_path, sr=None, offset=large_segment_start, duration=(large_segment_end - large_segment_start))
        
        small_segment_start = 0
        while small_segment_start < (large_segment_end - large_segment_start):
            cut_search_start = small_segment_start + min_length
            cut_search_end = min(small_segment_start + max_length, large_segment_end - large_segment_start)
            
            search_audio = large_segment_audio[int(cut_search_start * sr):int(cut_search_end * sr)]
            rms = librosa.feature.rms(y=search_audio, frame_length=2048, hop_length=512)[0]
            min_energy_frame = np.argmin(rms)
            cut_time_within_search = librosa.frames_to_time(min_energy_frame, sr=sr, hop_length=512)
            cut_time = cut_search_start + cut_time_within_search
            
            if cut_time - small_segment_start < min_length:
                cut_time = small_segment_start + min_length
            cut_sample = int(cut_time * sr)
            
            segment_to_save = large_segment_audio[int(small_segment_start * sr):cut_sample]
            segment_resampled = librosa.resample(segment_to_save, orig_sr=sr, target_sr=16000)

            if segment_resampled.size > 0:
                output_file = os.path.join(output_dir, f"seg_{segment_count}.wav")
                try:
                    wav_write(output_file, 16000, (segment_resampled * 32767).astype(np.int16))
                    print(f"Created segment {segment_count} from {large_segment_start + small_segment_start:.2f}s to {large_segment_start + cut_time:.2f}s")
                except Exception as e:
                    print(f"Error writing segment {segment_count}: {e}")
            else:
                print(f"Skipping empty segment {segment_count}.")
            
            small_segment_start = cut_time
            segment_count += 1

def process_audio_files_in_nested_folder(input_folder, output_base_dir, large_segment_duration=720, min_length=10, max_length=15):
    """
    Processes all audio files in a nested folder structure, splits each file into large segments (e.g., 12 minutes),
    and within each large segment, splits by the lowest energy points in 10-15 second intervals. Resamples each segment
    to 16 kHz and saves the segments in separate directories for each file.
    """
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_base_dir, relative_path, os.path.splitext(filename)[0])

                if os.path.exists(output_dir) and len(os.listdir(output_dir)) > 0:
                    print(f"Skipping {file_path}: already processed.")
                    continue
                
                split_audio_by_lowest_energy(file_path, output_dir, large_segment_duration, min_length, max_length)

    print("All files have been processed, split into segments, and resampled to 16 kHz.")
=======
from pydub import AudioSegment

def convert_and_resample_audios(input_folder, output_folder):
    """
    Recursively converts audio files in a nested folder structure to .wav format 
    with a 16 kHz sample rate and saves them in a specified output folder, 
    preserving the directory structure.
    
    Args:
    input_folder (str): Path to the root folder containing the audio files.
    output_folder (str): Path to the root folder where converted files will be saved.
    """
    # Traverse through all files in the nested folder structure
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                input_file_path = os.path.join(root, filename)
                
                # Recreate the directory structure in the output folder
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                
                # Load the audio file
                audio = AudioSegment.from_file(input_file_path)
                
                # Resample to 16 kHz and export as .wav
                output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.wav")
                audio.set_frame_rate(16000).export(output_file_path, format="wav")
                
                print(f"Converted and resampled {filename} to {output_file_path}")

    print("All files have been converted and resampled.")
>>>>>>> 859f8238d6a0b8bbd057b74f45f83d836e522eef
