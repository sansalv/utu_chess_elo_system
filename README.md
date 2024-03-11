# UTU Chess Elo System

This is a system that handles and keeps track of our chess club's (Yliopistonmäen Shakkikerho at the University of Turku) games and player profiles. The chess club organizes events (tournaments/casual playing) every wednesday. The system keeps track of all games and player profiles in JSON databases (crypted in the Github page).

We implemented Elo rating system. Players get their Elo rating (that we named TYLO  = Turun yliopiston Elo) updated after every chess club's event.

## How to use

Use command `git clone` to clone this repository into your computer. After this, go to the home directory in terminal window with `cd utu_chess_elo_system` command. This is where everything is run.

**Setup and activate the virtual environment with these two commands:**
```bash
python -m venv .venv

./.venv/Scripts/activate
```
If you get error
<p style="color: red;">... cannot be loaded because running scripts is disabled on this system. ...</p>
you need to allow script executing:

1. Start terminal as an Administrator. 
2. Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned` if your computer does not run the activation script. You have activated the virtual environment when you see (.venv) in the beginning of the terminal row.

**Install the requirements into the virtual environment**
```bash
pip install -r requirements.txt
```

When everything is installed into the virtual environment, you can **run the program with**
```bash
python.exe ./source/main.py
```
You have to know the top secret password to access the crypted databases.

## How to update the code

When you install new package to the virtual environment, you have to update the requirements.txt with: `pip freeze > requirements.txt`. When you update the code, do `git add .` and `git commit -m "Improved ..."` and `git push origin dev_myname`. In the GitHub page you can do a pull-request to the master branch. Notice that the ".venv" and "decrypted_data" folders are in the ".gitignore".

