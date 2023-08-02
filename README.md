# Epsilion War ref-links generator.

TODO description.

### Links
[Telegram bot](http://t.me/epsa_ref_bot)

### Local setup
```shell
$ git clone git@github.com:esemi/epsa-reflink-bot.git
$ cd epsa-reflink-bot
$ python3.11 -m venv venv
$ source venv/bin/activate
$ pip install -U poetry
$ poetry install
```

### Run tests
```bash
$ pytest --cov=app
```

### Run linters
```bash
$ poetry run mypy app/
$ poetry run flake8 app/
```

### Run Telegram auth util
```bash
python -m app.auth
```

### Run Telegram bot
```bash
python -m app.bot
```
