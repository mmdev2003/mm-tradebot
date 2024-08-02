FROM python:3.10-alpine
WORKDIR /root/mm-tradebot

COPY /root/mm-tradebot .

RUN pip install -r /root/mm-tradebot/set_stop/requirements.txt --break-system-packages
CMD python3 /root/mm-tradebot/set_stop/main.py