import os
import shutil

from mutagen.mp3 import EasyMP3


# This function will only set the values of "album" and "artist" to nothing,
# if they are not empty already.
def remove_album_and_artist_values(audio_file):
    if "album" in audio_file:
        audio_file["album"] = [""]

    if "artist" in audio_file:
        audio_file["artist"] = [""]


# This function will iterate through all files recognized as MP3 in the specified path
# and will rename their metadata title to the same name as the file itself.
# It will also return a count of every file so it can be used in the "move_files_to_usb" function
# to help track the progress of the files copies.
def rename_songs(songs_path):
    for file in os.scandir(songs_path):
        if file.name.endswith(".mp3"):
            audio_file = EasyMP3(file)

            file_name = file.name[:-4]  # Remove the ".mp3" from the file name.
            audio_file["title"] = file_name

            remove_album_and_artist_values(audio_file)

            audio_file.save()

    _, _, files = next(os.walk(songs_path))  # Returns a list of all files in the path.
    return len(files)


# This function is responsible for deleting all songs folders, along with all of their contents,
# in the specified path. The if condition is used to prevent the deletion of unrelated folders,
# as well as the System Volume Information, which is a system folder.
def clean_usb_songs_content(usb_path):
    for folder in os.listdir(usb_path):
        folder_path = os.path.join(usb_path, folder)

        if folder_path.startswith(f"{usb_path}Songs"):
            print(f"Deleting {folder}...")
            shutil.rmtree(folder_path)


# This function is responsible for creating the songs folders and moving all the files from the
# source path to the destination path, which are the new usb songs folders.
def move_files_to_usb(usb_path, files_counter, songs_path):
    folder_counter = 1
    songs_folder_path = f"{usb_path}Songs {folder_counter}"
    os.makedirs(songs_folder_path)  # Here we create the first folder to start adding files to it.

    songs_counter = 0
    total_songs_counter = 0

    for file in os.scandir(songs_path):
        # 100 will be the limit of files in each folder. After reaching it, a new folder will be
        # created and the counter will reset to restart the cycle.
        if songs_counter >= 100:
            folder_counter += 1
            songs_folder_path = f"{usb_path}Songs {folder_counter}"
            os.makedirs(songs_folder_path)

            songs_counter = 0

        if file.name.endswith(".mp3"):
            source_path = os.path.join(songs_path, file.name)
            destination_path = os.path.join(songs_folder_path, file.name)

            shutil.copy2(source_path, destination_path)

            songs_counter += 1
            total_songs_counter += 1

            print(
                f"Total files: {files_counter} | "
                f"Files moved: {total_songs_counter} | "
                f"Files left: {files_counter - total_songs_counter} | "
                f"Progress: {((total_songs_counter / files_counter) * 100):.2f}%"
            )


def organize_files(usb_path, files_counter, songs_path):
    print("Starting folders deletion...")
    clean_usb_songs_content(usb_path)
    print("Folders deleted\n")

    move_files_to_usb(usb_path, files_counter, songs_path)


SONGS_PATH = r"C:\Users\Álvaro\Desktop\music"  # The path where your songs folder are located.
USB_PATH = r"E:"  # The path where your USB flash drive is located.

print("Renaming songs...")
files_counter = rename_songs(SONGS_PATH)
print("Songs renamed\n")

organize_files(USB_PATH, files_counter, SONGS_PATH)

print("\nProgram finished!")
