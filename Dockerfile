FROM python:3.9-slim

ENV OPENAI_API_KEY <your API key here>

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]