FROM node:alpine
WORKDIR /opt

COPY ./package.json ./

RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 8888

ENTRYPOINT ["npm", "run", "serve", "--", "--port", "9029", "--host", "0.0.0.0"]
