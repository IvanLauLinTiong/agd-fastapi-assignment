# FastAPI Assignment

## Prerequisite
- have python 3.10.7 installed
- use virtualenv is preferred

## Project Description
- A note can consist of 0 or many tags.
- A note has title, description and tags.
- A tag has name.
- A note can be added, edited, retrieved and deleted.

## Tasks
- install requirements into python environment
- create note_app
- create note model
- create tag model
- create note serializers
- create note views
    - To get list of all notes
    - To create a note
    - To allow modification to the existing note
- create tag views
    - To get list of all tags
    - To get a tag and its corresponding notes where it is used

## Project Setup

1. Install Postgresql locally and running the Postgresql service, then create a database namely `NoteApplicationDB`.

2. Rename `.env-sample` to `.env`, and update the `username` and `password` with your DB credentials created from step 1.

3. Create a python virtual environment and activate it, then install relevant python packages by running command below:
```
virtualenv venv -p python3.10.7
source venv/bin/activate

# or you are running on Window platform
# venv\Scripts\activate

pip install -r requirements.txt
```

4. Launch the app by running command below:
```
uvicorn app:app --host 0.0.0.0 --port 8000
```

5. Now you may interact with the app at `http://127.0.0.1:8000/docs`.
