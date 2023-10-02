FROM python:3.11

WORKDIR /aiogram_bot

COPY . /aiogram_bot

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]
