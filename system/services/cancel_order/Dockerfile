FROM python:3.10-alpine
WORKDIR /root/mm-tradebot

COPY /root/mm-tradebot .

RUN pip install --upgrade pip && pip install -r /root/mm-tradebot/cancel_order/requirements.txt --break-system-packages
CMD python3 /root/mm-tradebot/cancel_order/main.py