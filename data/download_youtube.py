import subprocess
import os
import argparse
import glob
import string
import yaml
from collections import Counter
from create_csv import create_csv

file_counter = Counter()

def read_yaml(file_name):
    with open(file_name, "r") as f:
        return yaml.load(f)


def clean_filename(filename):
    valid_chars = "-_%s%s" % (string.ascii_letters, string.digits)
    new_name = "".join(c for c in filename if c in valid_chars)
    new_name = new_name.replace(' ','_')
    return new_name


def download(language, source, source_name, source_type, output_path, max_downloads):

    output_path_raw = os.path.join(output_path, "raw", language)
    
    if source_type == "playlist":
        #if not os.path.exists(output_path_raw):
            #os.makedirs(output_path_raw)
        playlist_archive = os.path.join(output_path_raw, "archive.txt")

        print("Downloading {0} {1} to {2}".format(source_type, source_name, output_path_raw))
        command = """youtube-dl -i --download-archive {} --no-post-overwrites --max-downloads {} --extract-audio --audio-format wav {} -o "{}/%(title)s.%(ext)s" """.format(
            playlist_archive, max_downloads, source, output_path_raw)
        subprocess.call(command, shell=True)
    else:       
        if os.path.exists(output_path_raw):
            print("skipping {0} because the target folder already exists".format(output_path_raw))
        else:
            print("Downloading {0} {1} to {2}".format(source_type, source_name, output_path_raw))
            command = """youtube-dl -i --max-downloads {} --extract-audio --audio-format wav {} -o "{}/%(title)s.%(ext)s" """.format(max_downloads, source, output_path_raw)
            subprocess.call(command, shell=True)


    # Use ffmpeg to convert and split WAV files into 3 second parts
    output_path_segmented = os.path.join(output_path, "segmented", language)
    print(output_path_segmented)
    segmented_files = glob.glob(os.path.join(output_path_segmented, "*.wav"))
    print(segmented_files)
    if source_type == "playlist" or not os.path.exists(output_path_segmented):
        if not os.path.exists(output_path_segmented):
            os.makedirs(output_path_segmented)
            
        files = glob.glob(os.path.join(output_path_raw, "*.wav"))

        for f in files:

            cleaned_filename = clean_filename(os.path.basename(f))
            cleaned_filename = cleaned_filename[:-4]

            if source_type == "playlist":
                waves = [f for f in segmented_files if cleaned_filename in f]
                if len(waves) > 0:
                    continue

            output_filename = os.path.join(output_path_segmented, cleaned_filename + "_%03d.wav")

            command = ["ffmpeg", "-y", "-i", f, "-map", "0", "-ac", "1", "-ar", "16000", "-f", "segment", "-segment_time", "3", output_filename]
            subprocess.call(command)

    file_counter[language] += len(glob.glob(os.path.join(output_path_segmented, "*.wav")))



def download_user(language, user, output_path, max_downloads):
    user_selector = "ytuser:%s" % user
    download(language, user_selector, user, "user", output_path, max_downloads)


def download_playlist(language, playlist_name, playlist_id, output_path, max_downloads):
    download(language, playlist_id, playlist_name, "playlist", output_path, max_downloads)

def download_user_and_playlist(output_path, max_downloads):
    sources = read_yaml("sources.yml")
    for language, categories in sources.items():
        for user in categories["users"]:
            if user is None:
                continue
                
            download_user(language, user, output_path, max_downloads)
            
        for category in categories["playlists"]:
            if category is None:
                continue

            playlist_name = category
            playlist_id = category
            download_playlist(language, playlist_name, playlist_id, output_path, max_downloads)
    print(file_counter)
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--output', dest='output_path', default=os.getcwd(), required=True)
    parser.add_argument('--downloads', dest='max_downloads', default=1200)
    args = parser.parse_args()

    download_user_and_playlist(args.output_path, args.max_downloads)
    

    
