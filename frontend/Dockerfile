FROM node:18-alpine

LABEL MAINTAINER: Andrew Medvedev hydra1337channel@gmail.com

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

CMD ["npx", "next", "start", "-p", "3000"] 

