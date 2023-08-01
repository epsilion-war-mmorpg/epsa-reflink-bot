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

Create env file to override default config
```bash
cat > .env << EOF
debug=true
bot_token=U_TELEGRAM_TOKEN
EOF
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


### Run Telegram bot
```bash
python -m app.bot
```
