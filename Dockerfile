FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY app/ ./app/
COPY models/ ./models/
COPY utils/ ./utils/

EXPOSE 8000
EXPOSE 8501

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]