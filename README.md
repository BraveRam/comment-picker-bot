# comment-picker-bot
A bot for picking random comments from public Telegram channels.

# installation

docker build -t tg-comment-picker .

docker run --rm --env-file .env tg-comment-picker
