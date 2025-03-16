FROM node:16.15-alpine

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build