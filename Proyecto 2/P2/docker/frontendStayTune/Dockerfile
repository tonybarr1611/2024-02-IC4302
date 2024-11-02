# Could be changed
FROM node:22.8-bookworm AS build

WORKDIR /app

COPY app/. .

RUN npm install

RUN npm install react-router-dom@latest
RUN npm run build

FROM nginx:1.17.1-alpine
COPY --from=build /app/dist /usr/share/nginx/html

COPY app/nginx.conf /etc/nginx/conf.d/default.conf