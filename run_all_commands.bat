echo Starting training process...

cmd.exe /c "cd ngisopenapi && conda activate venv && python demo.py && conda deactivate && cd .."
cmd.exe /c "cd kartAI && conda activate gdal_env && kai.bat create_training_data -n small_test_area -c config/dataset/kartai.json --region training_data/regions/small_building_region.json && conda deactivate && cd .."
cmd.exe /c "cd kartAI && conda activate gdal_env && kai.bat train -dn small_test_area -m unet -cn test_small_area_unet -c config/ml_input_generator/ortofoto.json"
