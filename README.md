## Description
This is an attemp to generate a wordcloud from Amazon Instant Video Review. You can find the filke in the samples directory.

Therer is 2 pages :
 - 127.0.0.1:5000
 - 127.0.0.1:5000/autocomplete

The first URL will generate a wordcloud from the amazon review
The second will enable you to test an autocomplete engine using Elasticsearch from cities around the world.

## Usage

I recommand you to create a custom virtualenv with `pyenv` before installing the requirements.

To install the requirements : `pip install -r install/requirements.txt`

You must start `Elasticsearch` from docker using the command `docker-compose up`. There is also a `Kibana` container.

After that, you just need to run the `launch.sh` script. This will export some env variables for `Flask`


## Create the Data

Usage : `python3 import_data.py`
