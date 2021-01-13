FROM python:3.9-alpine

RUN python3 -m pip install -U pip
RUN python3 -m pip install -U pipenv

VOLUME /app
WORKDIR /app

COPY base_requirements.txt requirements.txt /app/

RUN python3 -m pip install -U -r base_requirements.txt

COPY setup.py compile.sh .bash_colors run.py Pipfile Pipfile.lock MANIFEST.in LICENSE.txt README.md /app/

#RUN pipenv install --dev --ignore-pipfile

COPY ./privex/ /app/privex/
COPY ./bin/ /app/bin/

RUN pip3 install -U .

VOLUME /data
WORKDIR /data

ENTRYPOINT [ "/usr/local/bin/csp-gen" ]
