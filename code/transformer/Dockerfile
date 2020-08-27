FROM gcr.io/trv-hs-src-conceptstream-stage/pipenv:v01
WORKDIR /app
ADD transformer/Pipfile /app/Pipfile
ADD transformer/Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system
COPY transformer/src/ /app/
RUN mkdir /app/common/
COPY common/ /app/common/
CMD python main.py