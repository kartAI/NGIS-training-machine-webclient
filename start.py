import subprocess

print('Starting download process...')

# makes the code work locally
subprocess.call(['cmd.exe', '/c', 'cd ngisopenapi && conda activate bachelor2023 && python demo.py && conda deactivate && cd ..'])
subprocess.call(['cmd.exe', '/c', 'cd kartAI && conda activate bachelor2023 && kai.bat create_training_data -n small_test_area -c config/dataset/kartai.json --region training_data/regions/small_building_region.json -eager True && conda deactivate && cd ..'])
subprocess.call(['cmd.exe', '/c', 'cd ngisopenapi && conda activate bachelor2023 && python deleteDB.py && conda deactivate && cd ..'])


# makes the code work for docker build
#subprocess.call(['sh', '-c', 'cd ngisopenapi && python demo.py && cd ..'])
#subprocess.call(['sh', '-c', 'cd kartAI && python3 -m kartai.tools create_training_data -n small_test_area -c config/dataset/kartai.json --region training_data/regions/small_building_region.json -eager True && cd ..'])
#subprocess.call(['sh', '-c', 'cd ngisopenapi && python deleteDB.py && cd ..'])


