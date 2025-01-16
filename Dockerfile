FROM python:3.9

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /blog_backend
ENV PYTHONPATH=/blog_backend
ENV FLASK_APP="app.py"
ENV FLASK_ENV="development"

COPY . /blog_backend

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=3308"]