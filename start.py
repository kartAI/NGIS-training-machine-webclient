# start.py code
# Check correct pathing for you computer to where anaconda is installed and all the way to the activate.

import subprocess

print('Starting training process...')
subprocess.call('start cmd.exe /k "%USERPROFILE%\\anaconda3\\Scripts\\activate && run_all_commands.bat"', shell=True)

