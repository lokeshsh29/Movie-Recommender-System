# Movie Recommender System

This repository contains a movie recommender example. Below are quick instructions to create a local Python virtual environment and install dependencies.

## Create and activate virtual environment (recommended)

An included helper script `venv_setup.sh` creates a `.venv` directory using Python's built-in venv module and optionally installs packages from `requirements.txt`.

1. Make the script executable (if not already):

   chmod +x venv_setup.sh

2. Create the virtual environment without installing packages (safe, offline):

   ./venv_setup.sh --skip-install

3. Activate the environment:

   source .venv/bin/activate

4. Install dependencies (if you skipped earlier or want to install now):

   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt

You can also run the setup script to create the venv and install packages in one step:

   ./venv_setup.sh

Notes:
- The script defaults to `python3`. Use `--python python3.11` to select another interpreter.
- Use `--venv-dir DIR` to change where the virtual environment is created.
