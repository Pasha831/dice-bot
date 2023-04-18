# Purpose of the project

The **main purpose** of this project is to record my experience and share it with future generations and friends of mine who would like to get familiar with [VPS](https://en.wikipedia.org/wiki/Virtual_private_server), CI/CD and other interesting staff. 

I want to concentrate on services and instruments that I used along the way and how I used them.

The main focus will be on:
- [Github Actions](https://docs.github.com/en/actions) and Dockerization: how to build and push containers from Github to Docker Hub automatically via straightforward CI pipeline
- [Yandex Cloud](https://cloud.yandex.com/en-ru/) service and it's virtual private servers
- Essential [Docker](https://www.docker.com/) skills: how to pull a Docker image from Docker Hub, how to start a Docker Container, and how to observe changes of the image on a server and preserve containers up-to-date all the time.


> Noticeable mention: I am not a professional DevOps engineer, Python developer and so on. I do not want to show off for someone, I just want to share useful knowledge.

# What's inside

This projects is based on a simple telegram bot, that asks the user to guess the value of a dice, and then shows information about his attempt: is it successful or not.

<img src="https://user-images.githubusercontent.com/46136468/232685618-5953c1d6-49f1-4263-b900-19a638f00d7b.png"  width="50%" height="50%">

The bot is still running and you can try it on your own by clicking [here](https://t.me/bigboi666bot).


# Github Actions: simple CI pipeline

At the very beginning of the project I wished I could alter my repository with bot, commit changes, push them to `master` branch and then Github automatically builds a docker image of the project and pushes it straight to Docker Hub, where I could pull the image wherever I want (in my case: on VPS in cloud).

In order to bring the idea to life I created a basic `.yml` script, which listens to changes of `master` branch and when the changes occured, perform these steps:
- launch a virtual machine on `ubuntu-latest` system
- login to Docker Hub using credentials from `Actions secrets and variables` inside the repository ([how to manage secrets inside a repository](https://docs.github.com/en/codespaces/managing-codespaces-for-your-organization/managing-encrypted-secrets-for-your-repository-and-organization-for-github-codespaces))

<img src="https://user-images.githubusercontent.com/46136468/232688732-8473487d-e243-4841-8a13-c2daecb3d96b.png"  width="75%" height="50%">

- build a docker image of the project called `bot` with `lastest` tag added to it and then push it to Docker Hub

So, here is a .yml file which helps me to perform all these operations (you can also find inside .github/workflows folder, right [here](https://github.com/Pasha831/dice-bot/blob/master/.github/workflows/blank.yml))

```yml
name: CI

on:
  push:
    branches: [ "master" ]
    
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      
      - name: Docker Login
        uses: docker/login-action@v2.1.0
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
          
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/bot:latest
```

Thus, this Github Action allows me to update my [docker image](https://hub.docker.com/repository/docker/pasha831/bot/general) on Docker Hub:

<img src="https://user-images.githubusercontent.com/46136468/232690348-96c86cf6-f686-47d4-a6ca-1c2dc3dae4e3.png"  width="50%" height="50%">
