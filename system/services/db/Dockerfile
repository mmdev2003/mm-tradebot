FROM python:3.12-alpine
WORKDIR $ROOT_PATH

COPY . .

RUN export PYTHONPATH=$PYTHONPATH:$ROOT_PATH && pip install -r db/requirements.txt
CMD python3 db/init_db.py