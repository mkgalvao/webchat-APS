# APS-chat-Websockets
Esse repositório faz parte do trabalho de APS da UNIP 1/2019 

[Demo Online](https://aps-chat-websockets.herokuapp.com/)

## Montando o ambiente de desenvolvimento

1. Crie uma grátis conta no Heroku: https://heroku.com
1. Instale o heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
1. Crie sua app Heroku:
   ```bash
   $ heroku create

   Creating limitless-ocean-5046... done, stack is heroku-18
   http://limitless-ocean-5046.herokuapp.com/ | git@heroku.com:limitless-ocean-5046.git
   Git remote heroku added
   ```
1. Faça o deploy com um push:
   ```bash
   $ git push heroku master

    Counting objects: 113, done.
    ...
    Total 113 (delta 60), reused 0 (delta 0)

    -----> Python app detected
    ...
    http://your-app-123.herokuapp.com deployed to Heroku
   ```

Parabéns! Sua app está rodando no Heroku no endereço do output (ex: http://your-app-123.herokuapp.com).

