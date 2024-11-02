from pytube import YouTube
import moviepy.editor as moviepy
import ffmpeg
import os

# General Constants:
FOLDER = "%s\desktop" % os.getenv('userprofile')
ERROR_LOG = '\n~~~~~~~~~~~~~~~~~~~~~~~~~\nError with the given url!\n~~~~~~~~~~~~~~~~~~~~~~~~~\n'
FORBIDDEN_CHARS = {':', '/', '\\', '*', '?', '"', '<', '>', '|', '.'}
ENTER_URL = 'Enter a youtube url: '
AUDIO_FILENAME = '%s - %s - AUDIO.mp4'
VIDEO_FILENAME = '%s - %s - VIDEO.mp4'
FINAL_FILENAME = '%s - %s - FINAL.mp4'
DEFAULT_STR = "%s\\%s"
COLOR_GREEN = 'color a'
RESOLUTION = 'resolution'
ABR = 'abr'
PAUSE = 'pause'
MP4 = 'mp4'
MP3 = 'mp3'


# Removes problematic chars from both video title & author name
def clean_forbidden_chars(string):
    return ''.join(char for char in string if char not in FORBIDDEN_CHARS)


# Creates output folder and defines the output file path.
def set_output_path(video_title, video_author):
    # Removes problematic chars from both video title & author name
    cleaned_video_title = clean_forbidden_chars(video_title)
    cleaned_video_author = clean_forbidden_chars(video_author)

    # Creates output folder
    folder_path = DEFAULT_STR % (FOLDER, cleaned_video_title)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # Defines audio-only, video-only & both-combined files paths
    audio_only_filename = DEFAULT_STR % (folder_path, AUDIO_FILENAME % (cleaned_video_title, cleaned_video_author))
    video_only_filename = DEFAULT_STR % (folder_path, VIDEO_FILENAME % (cleaned_video_title, cleaned_video_author))
    final_filename = DEFAULT_STR % (folder_path, FINAL_FILENAME % (cleaned_video_title, cleaned_video_author))

    return audio_only_filename, video_only_filename, final_filename


# Gets a YouTube url, downloads and saves 3 file out of it: audio-only, video-only & both-combined.
def download_video():
    # Extracts the best audio & video streams
    video_url = input(ENTER_URL)
    yt = YouTube(video_url)
    best_video_quality = yt.streams.filter(file_extension=MP4).order_by(RESOLUTION).last()
    best_audio_quality = yt.streams.filter(only_audio=True, file_extension=MP4).order_by(ABR).last()

    # Sets the output paths of the just-retrieved audio & video streams, as well as the combined one.
    temp_audio_filename, temp_video_filename, final_combined_file = set_output_path(yt.title, yt.author)

    # Saves the raw audio & video files
    final_audio_only_file = best_audio_quality.download(filename=temp_audio_filename)
    final_video_only_file = best_video_quality.download(filename=temp_video_filename)

    # # Converts the raw audio & video files to mp3 & mp4 formats
    # final_audio_only_file = convert_to_mp(temp_audio_filename, best_audio_quality.subtype, MP3)
    # final_video_only_file = convert_to_mp(temp_video_filename, best_video_quality.subtype, MP4)
    #
    # Saves a combined version video file of both the mp3 & mp4 files
    video_stream = ffmpeg.input(final_audio_only_file)
    audio_stream = ffmpeg.input(final_video_only_file)
    ffmpeg.output(audio_stream, video_stream, final_combined_file).run()


# Gets a given audio/video file and saves it as a new mp3/mp4 file respectively.
def convert_to_mp(input_temp_filepath, current_ext, mp_ext):
    clip = ''
    # The new mp3/mp4 file name
    output_filename = input_temp_filepath.replace(current_ext, mp_ext)
    try:
        # Video Files
        clip = moviepy.VideoFileClip(input_temp_filepath)
        clip.write_videofile(output_filename)
    except:
        # Audio Files
        clip = moviepy.AudioFileClip(input_temp_filepath)
        clip.write_audiofile(output_filename)
    finally:
        clip.close()

    return output_filename


# Downloads a YouTube video as both mp4 and mp3 files.
def download_and_convert():
    download_video()


# The script is executed.
if __name__ == "__main__":
    try:
        os.system(COLOR_GREEN)
        download_and_convert()
    except Exception as e:
        print(ERROR_LOG)
        print(e)
    finally:
        os.system(PAUSE)
