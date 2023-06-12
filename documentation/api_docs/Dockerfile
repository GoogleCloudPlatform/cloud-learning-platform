FROM node:16.17.0-alpine as builder
ARG API_DOMAIN
ARG FIREBASE_API_KEY
ARG FIREBASE_AUTH_DOMAIN
ARG PROJECT_ID

WORKDIR /opt
COPY . .
RUN npm install --legacy-peer-deps
RUN npm run build

FROM nginx:1.21.1-alpine
RUN rm -rf /usr/share/nginx/html/* && rm -rf /etc/nginx/nginx.conf
COPY --from=builder /opt/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /opt/build /usr/share/nginx/html/docs
