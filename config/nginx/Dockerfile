FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY fullchain.pem /etc/letsencrypt/live/whaling-vote.kro.kr/fullchain.pem
COPY privkey.pem /etc/letsencrypt/live/whaling-vote.kro.kr/privkey.pem