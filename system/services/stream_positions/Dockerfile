FROM python:3.10-alpine
WORKDIR /root/mm-tradebot

COPY . .

RUN pip install -r /root/mm-tradebot/stream_positions/requirements.txt --break-system-packages
CMD python3 /root/mm-tradebot/stream_positions/main.py