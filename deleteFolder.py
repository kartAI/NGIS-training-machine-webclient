import os
import shutil

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f'Slettet mappe: {folder_path}')
    else:
        print(f'Mappen finnes ikke: {folder_path}')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

training_data_folder = os.path.join(BASE_DIR, "kartAI", "training_data", "Training_data")
folder_2 = os.path.join(BASE_DIR, "kartAI", "training_data", "created_datasets")
folder_3 = os.path.join(BASE_DIR, "kartAI", "training_data", "OrtofotoWMS")

def main():
    print("Starter sletting av mapper...")
    delete_folder(training_data_folder)
    delete_folder(folder_2)
    delete_folder(folder_3)
    print("Sletting av mapper fullført.")

if __name__ == "__main__":
    main()

# deleteFolder.py

def delete_all_folders():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    training_data_folder = os.path.join(BASE_DIR, "kartAI", "training_data", "Training_data")
    folder_2 = os.path.join(BASE_DIR, "kartAI", "training_data", "created_datasets")
    folder_3 = os.path.join(BASE_DIR, "kartAI", "training_data", "OrtofotoWMS")

    print("Starter sletting av mapper...")
    delete_folder(training_data_folder)
    delete_folder(folder_2)
    delete_folder(folder_3)
    print("Sletting av mapper fullført.")
