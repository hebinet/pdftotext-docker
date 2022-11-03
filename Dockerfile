FROM alpine:3.16

RUN addgroup --system pdftotext \
     && adduser --system --ingroup pdftotext pdftotext

RUN apk add --no-cache \
    py3-aiohttp \
    poppler-utils

ENV PYTHONUNBUFFERED 1
WORKDIR /app
USER pdftotext

EXPOSE 8080

COPY pdftotext.py .
CMD ["python3", "pdftotext.py"]
