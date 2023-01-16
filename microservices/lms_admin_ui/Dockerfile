FROM node:16.17.0-alpine as builder
WORKDIR /app
COPY . .

RUN npm install
ARG API_DOMAIN
RUN echo "${API_DOMAIN}"
ENV API_DOMAIN="${API_DOMAIN}"
RUN npm run build

FROM nginx:1.17.10-alpine
RUN rm -rf /usr/share/nginx/html/* && rm -rf /etc/nginx/nginx.conf
COPY --from=builder /app/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist/lms_admin_ui /usr/share/nginx/html