FROM gcr.io/trv-hs-src-conceptstream-stage/pipenv:v01
WORKDIR /app
ADD consumer/Pipfile /app/Pipfile
ADD consumer/Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system
COPY consumer/src/ /app/
RUN mkdir /app/common/
COPY common/ /app/common/
CMD python main.py