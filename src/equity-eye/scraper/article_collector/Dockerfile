FROM python:3.10.9-slim-buster

COPY src .
COPY requirements.txt .

RUN python -m venv /py && \
    apt-get update && \
    apt-get install vim -y && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

ENV PATH="/py/bin:$PATH"

RUN python -m spacy download en_core_web_sm

RUN chmod +x main_scraper.py && \
    chmod +x bbc_scraper.py && \
    chmod +x business_insider_scraper.py && \
    chmod +x washington_post_scraper.py && \
    chmod +x financial_post_scraper.py && \
    chmod +x nbc_news_scraper.py
CMD sleep 1d
