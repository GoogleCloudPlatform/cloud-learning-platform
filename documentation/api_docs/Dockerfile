FROM node:alpine
ARG API_DOMAIN
ARG FIREBASE_API_KEY
ARG FIREBASE_APP_ID
ARG PROJECT_ID
WORKDIR /opt

COPY ./package.json ./

RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 8888

ENTRYPOINT ["npm", "run", "serve", "--", "--port", "8888", "--host", "0.0.0.0"]
