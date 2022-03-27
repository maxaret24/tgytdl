FROM python:3.9-slim

WORKDIR /app
ARG API_ID
ARG API_HASH
ARG BOT_TOKEN
ARG LOG_GRP_ID=0
ENV API_ID=${API_ID} API_HASH=${API_HASH} BOT_TOKEN=${BOT_TOKEN} LOG_GRP_ID=${LOG_GRP_ID}

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["bash","start.sh"]