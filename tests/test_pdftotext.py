import os.path
import pytest
import requests
import shlex
import socket
import subprocess
import time


def test_convert_pdf_to_text(pdftotext, pdf):
    with open(pdf, 'rb') as pdf_file:
        resp = requests.post(pdftotext, files={'pdf': pdf_file})

    assert resp.status_code == 200
    assert resp.headers['Content-Type'] == 'text/plain'
    assert 'Postbank\nCard Service Hamburg' in resp.text


def test_convert_without_multipart_request(pdftotext):
    resp = requests.post(pdftotext)

    assert resp.status_code == 400
    assert resp.text == 'Multipart request required.'


def test_convert_without_pdf(pdftotext):
    resp = requests.post(pdftotext, files={'foo': 'bar'})

    assert resp.status_code == 400
    assert resp.text == 'No pdf provided.'


def test_convert_with_invalid_pdf(pdftotext):
    resp = requests.post(pdftotext, files={'pdf': 'bar'})

    assert resp.status_code == 500
    assert resp.text.startswith('Conversion failed.')


@pytest.fixture(scope="module")
def pdftotext():
    """Builds the docker image, starts the container and returns its URL.
    """
    context = os.path.dirname(os.path.dirname(__file__))
    run(f'docker build -t pdftotext:latest {context}')
    port = find_free_port()
    run(f'docker run -d -p {port}:8080 --name pdftotext pdftotext:latest')
    wait_until_ready(f'http://localhost:{port}/healthcheck')
    yield f'http://localhost:{port}'
    run('docker stop pdftotext')
    run('docker rm pdftotext')


@pytest.fixture(scope="module")
def pdf():
    return os.path.join(os.path.dirname(__file__), 'sample.pdf')


def wait_until_ready(url, timeout=10):
    start = now = time.time()
    while now - start < timeout:
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            return True
        time.sleep(0.1)
        now = time.time()
    return False


def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def run(cmd):
    args = shlex.split(cmd)
    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode != 0:
        pytest.fail(proc.stderr, pytrace=False)
