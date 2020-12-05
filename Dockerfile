FROM nikolaik/python-nodejs:python3.8-nodejs15

COPY ./ /app
WORKDIR /app/frontend
RUN npm install
RUN npm run build

WORKDIR /app/backend
RUN pip install -r /app/requirements.txt

EXPOSE 10010

CMD ["uvicorn", "main:app", "--port", "10010"]
