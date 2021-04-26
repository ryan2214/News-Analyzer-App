# News-Analyzer-App
Team 20

# Setup Network and nlp key
$env:HTTPS_PROXY="http://127.0.0.1:1080"

$env:GOOGLE_APPLICATION_CREDENTIALS="your-key.json"

# Method

![image](https://user-images.githubusercontent.com/12250414/116084644-964d7880-a6d0-11eb-8034-e49971132fa3.png)

Upload File, Manage Files, Check NLP Result and Search Keyword-Related News

# File Upload

![image](https://user-images.githubusercontent.com/12250414/116084912-d9a7e700-a6d0-11eb-9105-69fbf8413250.png)
Choose file, and server receives the file, parses and saves it to sqlite3 database.

# Manage Files

![image](https://user-images.githubusercontent.com/12250414/116085068-05c36800-a6d1-11eb-850c-94882ea1fb29.png)

Browse through all the files uploaded and news searched, could open and delete file by file name.

# Check NLP Result

![image](https://user-images.githubusercontent.com/12250414/116085240-34414300-a6d1-11eb-8eff-312a89448014.png)

During File upload process, we call the nlp API and save the NLP result with the file info in database. Now, use query to show the results.

# Search News

![image](https://user-images.githubusercontent.com/12250414/116085519-7b2f3880-a6d1-11eb-8026-f5f812a9604d.png)

Call newsapi to search from the Internet about the input keyword, show the first result and save it to the database.

May choose how many news listed.
