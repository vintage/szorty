## Szorty - web Django app for URLs shortening

1. Install all required dependencies:
*pip install -r requirements.txt*

2. Setup database
*./manage.py migrate*

3. Import words for URL shortening from text file into database. Each word should be placed in new line.
*./manage.py import_words <file_path>*
If you don't have word file with you, you can import the default one using:
*./manage.py import_words szorty/static/words.txt*

4. Run the server using
*./manage.py runserver localhost:8000*

5. Open your webbrowser and point to
*http://localhost:8000*