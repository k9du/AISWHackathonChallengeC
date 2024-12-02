## Steps to run the program (after cloning the repo)

1. Create a python virutal environment by running `python3 -m venv venv`
2. Activate the environment by running `source venv/bin/activate` on linux or `.\venv\Scripts\activate`
3. Install the requirements by running `pip install -r requirements.txt`
4. Create a .env file under the server directory.
5. Add your OPENAI_API_KEY and a FOLDER_PATH variable which defined where the data is located, in this case AISWHackathonChallengeC/resources/challenge_c/3_OpenDroneMap
6. Run the script for creating metadata by typing `python server/app/main.py` and wait for the script to finish (could take some amount of minutes) 
7. To run python server run `flask --app app.py run` 
8. Go to localhost:5000 and enjoy your life.


