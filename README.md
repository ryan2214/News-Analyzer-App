# News-Analyzer-App
Team 20

# Setup Network and nlp key
$env:HTTPS_PROXY="http://127.0.0.1:1080"

$env:GOOGLE_APPLICATION_CREDENTIALS="your-key.json"

# Run

python ./runserver.py

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

![image](https://user-images.githubusercontent.com/12250414/116087578-956a1600-a6d3-11eb-869a-8261926d5373.png)

During File upload process, we call the nlp API and save the NLP result with the file info in database. Now, use query to show the results.

# Search News

![image](https://user-images.githubusercontent.com/12250414/116087482-7bc8ce80-a6d3-11eb-9edb-ce8a7b3acbd1.png)

Call newsapi to search from the Internet about the input keyword, show the first several results and save it to the database.

*May choose how many news listed, but NLP will take a large amount of time if set to a big list.*

# Database Table
![image](https://user-images.githubusercontent.com/12250414/116092432-63a77e00-a6d8-11eb-8e79-dd60e4e0b9fe.png)

It doesn't feel good to store 2 kinds of objects in 1 table, but now it is.

Files use file_name as index, news uses title as index.
