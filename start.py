import subprocess

subprocess.call(['sh', '-c', 'cd ngisopenapi && python demo.py && cd ..'])
subprocess.call(['sh', '-c', 'cd kartAI && ./kai create_training_data -n small_test_area -c config/dataset/kartai.json --region training_data/regions/small_building_region.json && cd ..'])
subprocess.call(['sh', '-c', 'cd kartAI && ./kai train -dn small_test_area -m unet -cn test_small_area_unet -c config/ml_input_generator/ortofoto.json'])
