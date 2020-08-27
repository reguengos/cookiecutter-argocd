FROM gcr.io/trv-hs-src-conceptstream-stage/pipenv:v01
WORKDIR /app
ADD producer/Pipfile /app/Pipfile
ADD producer/Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system
COPY producer/src/ /app/
RUN mkdir /app/common/
COPY common/ /app/common/
CMD python main.py