# **PIX  Challenge** #
Repositório com o client/consumer do desafio do pix do Nubank

# **usefull stuffs - MiniKube** #

## Carregar imagem local para o minikube ##
minikube image load pix-challenge-consumer:latest
minikube image load pix-challenge-server:latest

## Expor interface gráfica do RabbitMQ ##
minikube service rabbitmq --url -n pix-challenge