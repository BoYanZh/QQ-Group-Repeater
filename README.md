# QQGroupRepeater

A chat bot for QQ group based on ~~CoolQ~~ python-aiocqhttp, using cqhttp protocol.

## Usage

### Deployment of cqhttp backend (using go-cqhttp)

Due to the policy of tencent, the bot is currently using [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) as cqhttp backend. And it is just an example. You can refer to the documentation of go-cqhttp for more details.

The [`config.yml`](https://docs.go-cqhttp.org/guide/config.html) for go-cqhttp may looks like this:

```yml
account: 
  uin: ID 
  password: 'pass' 
  encrypt: false  
  status: 0      
  relogin: 
    delay: 3   
    interval: 3   
    max-times: 5  
  use-sso-address: false

heartbeat:
  interval: 5

message:
  post-format: string
  ignore-invalid-cqcode: false
  force-fragment: false
  fix-url: false
  proxy-rewrite: ''
  report-self-message: false
  remove-reply-at: false
  extra-reply-data: false

output:
  log-level: warn
  debug: false 

default-middlewares: &default
  access-token: ''
  filter: ''
  rate-limit:
    enabled: false 
    frequency: 1  
    bucket: 1     

database: 
  leveldb:
    enable: true

servers:

  - http:
      host: 127.0.0.1
      port: 5700
      timeout: 5
      middlewares:
        <<: *default 
      post:
  - ws:
      host: 127.0.0.1
      port: 6700
      middlewares:
        <<: *default 
  - ws-reverse:
      universal: ws://127.0.0.1:8090/ws/
      reconnect-interval: 3000
      middlewares:
        <<: *default 
  - pprof:
      host: 127.0.0.1
      port: 7700

```

Check the port and then launch go-cqhttp. The ws-reverse connection may fail until the starting of bot.The go-cqhttp is not that stable so I add a crontab to restart it every 30 minutes.

### Start the bot

Run commands in terminal:

```bash
pip install -r requirements.txt
cp settings.json.example settings.json
vim settings.json #configure
python3 coolq.py
```

Enjoy it!

### Build the docs

First install `mkdocs-material`
```bash
pip install mkdocs-material
```

* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Credit

- [CoolQ](https://cqp.cc/)
- [python-aiocqhttp](https://github.com/richardchien/python-aiocqhttp)
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

## Contributing

If you have any ideas or find some bugs, please raise a [issue](https://github.com/BoYanZh/QQGroupRepeater/issues).
