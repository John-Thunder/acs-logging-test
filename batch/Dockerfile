FROM rgardler/acs-logging-test-base

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY src src

CMD [ "python", "src/batch.py" ]