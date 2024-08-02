FROM python:3.12-alpine
WORKDIR $ROOT_PATH

COPY . .

RUN export PYTHONPATH=$PYTHONPATH:$ROOT_PATH && pip install -r open_position/requirements.txt
CMD python3 open_position/main.py