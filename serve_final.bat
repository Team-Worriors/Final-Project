cd C:\Final_Project
git pull https://%TESTAPP_GIT_PAT%@github.com/Team-Worriors/Final-Project.git
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe server.py
