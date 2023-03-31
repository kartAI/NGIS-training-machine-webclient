# start.py code

import subprocess

print('Starting training process...')
subprocess.call(['cmd.exe', '/c', 'cd ngisopenapi && conda activate venv && python demo.py && conda deactivate && cd ..'])
subprocess.call(['cmd.exe', '/c', 'cd kartAI && conda activate gdal_env && kai.bat create_training_data -n small_test_area -c config/dataset/kartai.json --region training_data/regions/small_building_region.json && conda deactivate && cd ..'])
subprocess.call(['cmd.exe', '/c', 'cd kartAI && conda activate gdal_env && kai.bat train -dn small_test_area -m unet -cn test_small_area_unet -c config/ml_input_generator/ortofoto.json'])





#Teste dette 

# get the absolute path to the directory containing start.py
#root_dir = Path(__file__).resolve().parent.parent

# construct the paths to the ngisopenapi and kartAI directories
#ngisopenapi_dir = root_dir / 'ngisopenapi'
#kartAI_dir = root_dir / 'kartAI'

# execute the commands
#subprocess.call(['sh', '-c', 'cd ngisopenapi && python demo.py && cd ..'])
#subprocess.call(['sh', '-c', 'cd kartAI && ./kai create_training_data -n small_test_area -c config/dataset/kartai.json --region training_data/regions/small_building_region.json && cd ..'])
#subprocess.call(['sh', '-c', 'cd kartAI && ./kai train -dn small_test_area -m unet -cn test_small_area_unet -c config/ml_input_generator/ortofoto.json'])
