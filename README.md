# pdftotext

A dockerized webservice to convert Pdf files to Text.

## Description

pdftotext uses the linux tool pdftotext to extract the text.
It exposes just a single endpoint for uploading an .pdf file and returns the
extracted text. The webservice is written in Python using the aiohttp web server.

## Usage

To start the webservice just run
```
docker-compose up
```

The .pdf file must be uploaded as multipart/form-data with a part named `pdf`
containing the .pdf file.

Example:

```
curl -F "pdf=@tests/sample.pdf" http://localhost:3000/
```

## Testing

To execute the tests, Python 3.8 with pytest and requests is required.

```
python3.8 -m venv venv
./venv bin/activate
pip install pytest requests
```

Tests are run by executing pytest:

```
pytest
```
