# CEOS 15기 파트장 투표 어플리케이션

### [🗳 투표하러 가기](https://react-vote-14th-522lienzc-team-whaling.vercel.app/)

## 👏 소개

CEOS 14기 팀 웨일링이 제작한 15기 파트장 투표 어플리케이션의 백엔드 레포지토리입니다.

## ✔ 기능

**로그인**

- 사용자 로그인은 `JWT`를 통해 인증됩니다.

**회원가입**

- 아이디, 이메일, 비밀번호를 입력해 새로운 회원으로 가입할 수 있습니다.
- 아이디와 이메일의 `중복 체크`가 이루어집니다.

**투표**

- 투표 페이지에는 모든 후보자가 `득표수`를 기준으로 내림차순 정렬되어 보여집니다.
- `로그인 유저`만 투표가 가능합니다.
- 한 아이디 당 `한 번의 투표`만 가능합니다.

## 🌥 ERD

![vote-app-erd](https://user-images.githubusercontent.com/71026706/144714936-a7e91f9f-6dc2-4481-b0e0-a36bebb5309f.png)

**사용자 User**

- 회원가입 시 `아이디, 이메일, 비밀번호`를 받습니다.
- `아이디와 이메일`은 중복될 수 없습니다.
- `투표여부`는 한 아이디의 중복 투표를 방지하기 위한 필드이며 기본값 `false`로 설정됩니다.

**후보자 Candidate**

- 후보자들은 `득표수`를 기준으로 내림차순 정렬됩니다.
- 득표수가 같다면 `이름순`으로 정렬됩니다.

## [📑 API document](https://documenter.getpostman.com/view/18244416/UVJcjw8h)

API 문서는 Postman으로 제작되었으며 위 링크에서 확인하실 수 있습니다👍

## 🐳 Https 설정 과정

내도메인 한국에서 무료 도메인을 발급 받아서 사용했습니다.

이 과정에서 삽질을 좀 많이했습니다. 처음에는 certbot컨테이너를 한번 사용해서 인증서를 최초로 발급받는 식으로 하였는데, 무료 도메인을 사용하여서 그런지 오류가 자꾸 발생하였습니다. 그래서 다른 방식을 사용하였습니다.

설정했던 과정은

1. 무료 도메인 발급 받기

2. AWS EC2에 ssh 접속

3. certbot 설치 및 인증서 발급 받기 (nginx의 `nginx.conf` 파일 수정해놓음)
    1.  이 과정에서 무료 도메인이어서 인증서 발급이 안되는 에러가 발생
    2. `certbot certonly -d  내도메인 --manual --preferred-challenges dns`  이 명령어를 ec2에서 실행
    3. TXT가 출력되면 복사하여 도메인 관리에서 _acme-challenge를 txt 도메인이름으로 설정
    4. 이렇게 하면 나머지 과정이 완료가 됐습니다.

4. 인증서가 이제 `/etc/letsencrpyt/live/내도메인` 에 발급이 되었는데, 도커에서 참조하려고하니 왜인지 모르겠지만 자꾸 실패해서, 인증서를 다른 폴더에 옮겨 주었습니다.

5. 그리고 `.env.prod` 에 DJANGO_ALLOWED_HOST에 도메인을 추가하지 않으면 400 bad request가 계속 발생합니다. 꼭 추가해 주도록 합시다! (settings/base.py 에 ALLOWED_HOST에만 추가하면 안되더라고요..)

```python
# docker-compose.prod.yml
nginx:
    container_name: nginx
    build: ./config/nginx
    volumes:
      - static:/home/app/web/static
      - media:/home/app/web/media
      - /etc/letsencrypt/whalingkey:/etc/letsencrypt/live/www.whaling-vote.kro.kr
		ports:
      - "80:80"
      - "443:443"
```

이런식으로 nginx 컨테이너의 볼륨을 수정하여 키를 참조할 수 있도록 해주었습니다.(**포트도 꼭 열어주기**)

최종 `nginx.conf` 코드는 이렇습니다!

```python
# nginx.conf
upstream voteapp {
  server web:8000;
}
#http
server {
  listen 80;
  listen [::]:80;
  # Http로 들어온 요청을 Https로 바꿔줌

  server_name whaling-vote.kro.kr www.whaling-vote.kro.kr;

  location / {
    return 301 https://www.whaling-vote.kro.kr$request_uri;
  }
}
#https
server {
  listen 443 ssl;

  server_name whaling-vote.kro.kr www.whaling-vote.kro.kr;

  ssl_certificate     /etc/letsencrypt/live/www.whaling-vote.kro.kr/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/www.whaling-vote.kro.kr/privkey.pem;

  location / {
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $host;
    proxy_pass http://voteapp;
    proxy_redirect off;
  }
  location /static/ {
    alias /home/app/web/static/;
  }

  location /media/ {
    alias /home/app/web/media/;
  }
}
```

이렇게하고 빌드하니 인증이 되었습니다! 야호
