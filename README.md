# QQGroupRepeater

A chat bot for QQ group based on CoolQ and python-aiocqhttp.

## Usage

Install [CoolQ](https://cqp.cc/) and [python-aiocqhttp](https://github.com/richardchien/python-aiocqhttp). Run CoolQ HTTP API.

The configure file for CoolQ HTTP API may look as follows:

```json
{
    "host": "127.0.0.1",
    "port": 5700,
    "use_http": true,
    "post_url": "http://127.0.0.1:8090"
}
```

Then run commands in terminal:

```bash
cp settings.json.example settings.json
vim settings.json #configure
python3 coolq.py
```

Enjoy it!

## Credit

- [CoolQ](https://cqp.cc/)
- [python-aiocqhttp](https://github.com/richardchien/python-aiocqhttp)

## Contributing

If you have any ideas or find some bugs, please raise a [issue](https://github.com/BoYanZh/QQGroupRepeater/issues).
