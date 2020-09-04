FROM python:3-slim
RUN apk update && apt install -y git
# current pipenv is broken, and install --system does not work
# https://github.com/pypa/pipenv/issues/4344
RUN python -m pip install git+https://github.com/pypa/pipenv@97324a6932b3fda0ccbabcc349474d74a913e0bc