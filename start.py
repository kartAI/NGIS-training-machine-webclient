import subprocess

# makes the code work locally
print('Starting download process...')
subprocess.call(['cmd.exe', '/c', 'cd ngisopenapi && conda activate venv && python demo.py && conda deactivate && cd ..'])
subprocess.call(['cmd.exe', '/c', 'cd kartAI && conda activate gdal_env && kai.bat create_training_data -n small_test_area -c config/dataset/kartai.json --region training_data/regions/small_building_region.json -eager True && conda deactivate && cd ..'])
subprocess.call(['cmd.exe', '/c', 'cd ngisopenapi && conda activate venv && python deleteDB.py && conda deactivate && cd ..'])


# makes the code work for docker build
#print('Starting download process...')
#subprocess.call(['sh', '-c', 'cd ngisopenapi && python demo.py && cd ..'])
#subprocess.call(['sh', '-c', 'cd kartAI && python3 -m kartai.tools create_training_data -n small_test_area -c config/dataset/kartai.json --region training_data/regions/small_building_region.json -eager True && cd ..'])
#subprocess.call(['sh', '-c', 'cd ngisopenapi && python deleteDB.py && cd ..'])
