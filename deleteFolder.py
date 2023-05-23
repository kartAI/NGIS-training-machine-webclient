import os
import shutil

# Define function to delete a folder


def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # Delete folder and its contents
        print(f'Deleted folder: {folder_path}')
    else:
        print(f'The folder does not exist: {folder_path}')


# Get base directory of script file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths for folders to be deleted
training_data_folder = os.path.join(
    BASE_DIR, "kartAI", "training_data", "Training_data")
folder_2 = os.path.join(
    BASE_DIR, "kartAI", "training_data", "created_datasets")
folder_3 = os.path.join(BASE_DIR, "kartAI", "training_data", "OrtofotoWMS")

# Define main function to delete folders and their contents


def main():
    print("Starting deletion of folders...")
    delete_folder(training_data_folder)  # Delete first folder
    delete_folder(folder_2)  # Delete second folder
    delete_folder(folder_3)  # Delete third folder
    print("Folders were deleted successfully.")


# Check if script is being run directly (as opposed to being imported as a module)
if __name__ == "__main__":
    main()  # Call main function

# Define a second function that does the same thing as main


def delete_all_folders():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    training_data_folder = os.path.join(
        BASE_DIR, "kartAI", "training_data", "Training_data")
    folder_2 = os.path.join(
        BASE_DIR, "kartAI", "training_data", "created_datasets")
    folder_3 = os.path.join(BASE_DIR, "kartAI", "training_data", "OrtofotoWMS")
    print("Starting deletion of folders...")
    delete_folder(training_data_folder)
    delete_folder(folder_2)
    delete_folder(folder_3)
    print("Folders were deleted successfully.")
