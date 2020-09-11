# QQGroupRepeater



A chat bot for QQ group based on ~~CoolQ~~ python-aiocqhttp, using cqhttp protocol.

## Usage

### Deployment of cqhttp backend (using go-cqhttp)

Due to the policy of tencent, the bot is currently using [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) as cqhttp backend. And it is just an example. You can refer to the documentation of go-cqhttp for more details.

The `config.json` for go-cqhttp may looks like this:

```json
{
        "uin": 123456,
        "password": "654321",
        "encrypt_password": false,
        "password_encrypted": "",
        "enable_db": true,
        "access_token": "",
        "relogin": true,
        "relogin_delay": 3,
        "http_config": {
                "enabled": false,
                "host": "0.0.0.0",
                "port": 5700,
                "timeout": 0,
                "post_urls": {"0.0.0.0:8090": ""},
                "post_message_format": "string"
        },
        "ws_config": {
                "enabled": true,
                "host": "0.0.0.0",
                "port": 6700
        },
        "ws_reverse_servers": [
                {
                        "enabled": true,
                        "reverse_url": "ws://127.0.0.1:8090/ws/",
                        "reverse_reconnect_interval": 3000
                }
        ],
        "debug": false
}
```

Launch go-cqhttp. The go-cqhttp is not that stable so I add a crontab to restart it every 30 minutes.

### Start the bot

Run commands in terminal:

```bash
pip install -r requirements.txt
cp settings.json.example settings.json
vim settings.json #configure
python3 coolq.py
```

Enjoy it!

## Credit

- [CoolQ](https://cqp.cc/)
- [python-aiocqhttp](https://github.com/richardchien/python-aiocqhttp)
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

## Contributing

If you have any ideas or find some bugs, please raise a [issue](https://github.com/BoYanZh/QQGroupRepeater/issues).
