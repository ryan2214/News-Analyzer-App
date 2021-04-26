# News-Analyzer-App
Team 20

# Setup Network and nlp key
$env:HTTPS_PROXY="http://127.0.0.1:1080"

$env:GOOGLE_APPLICATION_CREDENTIALS="your-key.json"

# Run

python ./runserver.py

access: http://localhost:5555/

# Method

![image](https://user-images.githubusercontent.com/12250414/116111243-0c5dd980-a6e9-11eb-84b8-a78eae43cedc.png)

Upload File, Manage Files, Check NLP Result and Search Keyword-Related News

# File Upload

![image](https://user-images.githubusercontent.com/12250414/116111290-18499b80-a6e9-11eb-80a4-0d201bff59be.png)

Choose file, and server receives the file, parses and saves it to sqlite3 database.

# Manage Files

![image](https://user-images.githubusercontent.com/12250414/116111377-2e575c00-a6e9-11eb-90d4-59d496124495.png)

Browse through all the files uploaded and news searched, could open and delete file by file name.

# Check NLP Result

![image](https://user-images.githubusercontent.com/12250414/116111418-36170080-a6e9-11eb-90ee-dbf141388094.png)

During File upload process, we call the nlp API and save the NLP result with the file info in database. Now, use query to show the results.

# Search News

![image](https://user-images.githubusercontent.com/12250414/116111517-4e871b00-a6e9-11eb-884b-13b47acbd36e.png)

Call newsapi to search from the Internet about the input keyword, show the first several results and save it to the database.

*May choose how many news listed, but NLP will take a large amount of time if set to a big list.*

# Database Table
![image](https://user-images.githubusercontent.com/12250414/116092432-63a77e00-a6d8-11eb-8e79-dd60e4e0b9fe.png)

It doesn't feel good to store 2 kinds of objects in 1 table, but now it is.

Files use file_name as index, news uses title as index.
