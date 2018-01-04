# BallotAPI main website

This is the code that runs https://ballotapi.com/

## Installation

Here is how to run this website locally (for development, etc.).

1. Clone this repo.<br/>
`git clone https://github.com/sfbrigade/ballotapi`

2. Create a Python 3 virtual environment.<br/>
`virtualenv -p python3 ballotapi-website-venv`<br/>
`source ballotapi-website-venv/bin/activate`<br/>

3. Install the website dependencies.<br/>
`cd ballotapi/website/`<br/>
`pip install -r requirements.txt`

4. Start a development webserver.<br/>
`python3 manage.py runserver`

5. Done! This website should be running on http://localhost:8000/

## Upgrading

1. Update the website dependencies.<br/>
`pip install --upgrade -r requirements.txt`

## Testing

TODO

