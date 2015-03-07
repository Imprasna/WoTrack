# WoTrack: Spotify Words to Track (Poetic rewrite on non-matching)

## Description
A simple text to track generator. This application will process user input and find tracks that resemble the text pattern.
If some words or phrases are not found, then the application will generate the best poetic rewrite it can.

## How the processing works
This application combines natural language processing with dynamic programming to quickly and accurately
(still very much in its infancy) generate tracks from Spotify resembling the input text pattern. It does so
by:

1. Breaking the sentences down into trigrams and collecting the trigram collocations with
the highest PMI (Pointwise Mutual Information).

2. The trigram collocations are used as the search phrases (or queries) on Spotify's Track API.

3. The tracks are retrieved from Spotify and cached through Memcached.

4. The Levenshtein Distance between the track names and the search phrases is then determined and minimized.

5. The Levenshtein Distance determination/minimization step is done recursively until the input text is fully consumed.

6. If there were no good trigram phrase matches, then the remaining trigram collocations are decomposed into digrams and unigrams. The same logic is ran on each, respectively.

*Note* Order is currently not maintained in the demo frontend page.

## Setup
This is a self contained Python/Django application. Perform the following steps
to install the applications setup the environment and to install dependencies:

1. Install Memcached by following the instructions at: <http://memcached.org/downloads>

2. Install Python 2.7x on your target platform. Python 2.7x can be downloaded and installed from: <https://www.python.org/downloads/>

3. Install pip for Python. Instructions for doing so could be found at: <https://pip.pypa.io/en/latest/installing.html>

4. It is recommended to setup a virtual environement for your Python 2.7x interpreter. Instructions to doing so could be found at <http://docs.python-guide.org/en/latest/dev/virtualenvs/>

5. install all of the applications requirements by running the following commands in the project's root:
    i. pip install -r requirements.txt
    ii. pip install -r requirements-dev.txt

6. Setup caching by running the following command from the project's root:
    i. python manage.py createcachetable

7. Run the tests to confirm everything is working properly by running the following command in the project's root:
    i. invoke tests

8. To Setup the application's frontend assets run the following command:
    i. python manage.py collectstatic

9. Now we can run the frontend server on port 8000. From the project's root, run the following command:
    i. python manage.py runserver 8000

10. Finally, run your browser and go to the url: <http://localhost:8000>

## Running all tests
![alt tag](https://github.com/husman/WoTrack/blob/master/doc/images/tests.1.png)

## Running text to track processing without caching and with caching
![alt tag](https://github.com/husman/WoTrack/blob/master/doc/images/tests.2.png)

## Snapshots and Demostrations
Tracks with good match:
![alt tag](https://github.com/husman/WoTrack/blob/master/doc/images/demo.1.png)

Tracks with good match (Rewrite):
![alt tag](https://github.com/husman/WoTrack/blob/master/doc/images/demo.2.png)

Tracks with ok match (Rewrite)
![alt tag](https://github.com/husman/WoTrack/blob/master/doc/images/demo.3.png)

Tracks with not so great matching (Rewrite)
![alt tag](https://github.com/husman/WoTrack/blob/master/doc/images/demo.4.png)