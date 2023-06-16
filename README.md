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

As for bot token, I store it inside `.env` file on my VPS.

The bot is still running and you can try it on your own by clicking [here](https://t.me/bigboi666bot).


# Github Actions: simple CI pipeline

At the very beginning of the project I wished I could alter my repository, commit changes, push them to `master` branch and then Github automatically executes tests, checks the code, builds a docker image of the project and pushes it straight to Docker Hub, where I could pull the image wherever I want (in my case: on VPS in cloud).

In order to bring the idea to life I've created 2 basic `.yml` scripts, where **former** is responisble for script building, test running and checking code style, whereas **latter** listens to changes of `master` branch and when the changes occured, perform these steps:
- launch a virtual machine on `ubuntu-latest` system
- login to Docker Hub using credentials from `Actions secrets and variables` inside the repository ([how to manage secrets inside a repository](https://docs.github.com/en/codespaces/managing-codespaces-for-your-organization/managing-encrypted-secrets-for-your-repository-and-organization-for-github-codespaces))

<img src="https://user-images.githubusercontent.com/46136468/232688732-8473487d-e243-4841-8a13-c2daecb3d96b.png"  width="75%" height="50%">

- build a docker image of the project called `bot` with `lastest` tag added to it and then push it to Docker Hub

## Build & Push Docker image

So, here is a `.yml` file which helps me to perform all these operations (you can also find inside .github/workflows folder, right [here](https://github.com/Pasha831/dice-bot/blob/master/.github/workflows/blank.yml))

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

<img src="https://user-images.githubusercontent.com/46136468/232690348-96c86cf6-f686-47d4-a6ca-1c2dc3dae4e3.png"  width="75%" height="50%">

## Testing and Linting

I've also wrote a simple `.yml` script to install all the requirements from `requirements.txt`, execute tests with [`pytest`](https://docs.pytest.org/en/7.3.x/) and check the validity and following to [PEP8](https://peps.python.org/pep-0008/) of my code using [`pylint`](https://pypi.org/project/pylint/).

So, here's the script:

```yml
name: Test&Lint

on:
  push:
    branches: [ "master" ]
  pull_request:
    branches: [ "master" ]

  workflow_dispatch:

jobs:
  test_and_lint:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Test with pytest
        run: pytest test_code.py
      
      - name: Lint with pylint
        run: pylint main.py
        
```

That's the example of perfectly working pipeline with no bugs and erros in code, as well as without deviations from renowned code style:

![image](https://github.com/Pasha831/dice-bot/assets/46136468/ced0206c-f315-47dc-9eb0-85f03987b819)

# Yandex Cloud, it's VPSs and pricing

I decided to use [Yandex Cloud](https://cloud.yandex.com/en-ru/) to create my own VPS where the bot will be running. I understand, that there are lots of cheaper and better clouds on the web, but this one was a perfect choice for a newbie like me because of its simplicity in creation and use.

Yandex Cloud provides you with **4000** rouble grand for the creation of an account and your first cloud machine. However, there are some nuances:

<img src="https://user-images.githubusercontent.com/46136468/232693604-39a1073b-c4fe-42e7-9089-f6f89300e534.png"  width="75%" height="50%">

Unfortunately, you only have 1000 rubles for your virtual private machine and 3000 rubles for other (not so crucial) services. Therefore, keep an eye on the consumption of your VPS and wisely choose suitable parametrs for your machine.

My machine costs me approximately 2500 rubles per month and consists of 2 CPUs, 4 gb of RAM and 32 gb of HDD:
<img src="https://user-images.githubusercontent.com/46136468/232696723-1bb3ddd4-eb0a-4c1f-b024-cf78833122ce.png"  width="25%" height="25%">

Here, I don't want to dive in details of a creation and seting up of VPS and will provide you with complete and clear instructions by Yandex itself:
- [How to create a Linux VM](https://cloud.yandex.com/en-ru/docs/compute/quickstart/quick-create-linux)
- [How to establish a connection](https://cloud.yandex.com/en-ru/docs/compute/operations/vm-connect/ssh) to the VPS via [ssh](https://en.wikipedia.org/wiki/Secure_Shell) and also [how to add other users to the VM](https://cloud.yandex.com/en-ru/docs/compute/operations/vm-connect/ssh#vm-authorized-keys)

In addition, I want to share the instruction [how to connect to VM using SSH via Visual Studio Code](https://code.visualstudio.com/docs/remote/ssh-tutorial).

> Noticeable mention: at this moment I ran out of money on my Yandex Cloud account, so I had decided to switch to another VPS provied. I would recommend you to use [MTS Cloud](https://cloud.mts.ru/en/), because these guys provide you **5000** rouble grand after the first payment (500+ russian rubles).

# Docker: update running containers to latest images

It is not a rocket science [how to build a docker image](https://docs.docker.com/engine/reference/commandline/build/).

For this project, `Dockerfile` has to pull `python3` image, copy `requirements.txt` and then download all dependecies via `pip install` command with `-r` flag, that's all:
 ```Dockerfile
 FROM python:3.9-slim as compiler

WORKDIR /app/
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
 ```

On your virtual machine you can freely [login to Docker Hub](https://stackoverflow.com/questions/57108005/login-to-docker-hub-by-command-line), [pull the image](https://docs.docker.com/engine/reference/commandline/pull/) and then [start it](https://docs.docker.com/engine/reference/commandline/run/) via `docker run` command:
```cmd
docker run -d pasha831/bot:latest
```

However, there is a noticeable drawback of this approach: you have to manually [stop your container](https://docs.docker.com/engine/reference/commandline/stop/) when the corresponding image is updated, [manually update the image](https://phoenixnap.com/kb/update-docker-image-container) and then launch again your container.

It's a huge waist of time and effort which could be optimized by some automatization proccess.

There is a quite clear instruction how to [Automatically Update Docker Container Images with Watchtower on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-automatically-update-docker-container-images-with-watchtower-on-ubuntu-22-04). You also have to know how to work with [Docker Compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04).

Here is a `docker-compose.yml` file which launches bot container with `.env` file with its token as a parameter and also launches [Watchtower](https://github.com/containrrr/watchtower) container to observe any updates of former container on Docker Hub:
```yml
version: "3"
services:
  bot:
    image: pasha831/bot:latest
    container_name: bot-container
    env_file:
      - .env

  watchtower:
    image: containrrr/watchtower
    container_name: watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 86400 bot-container
```

`command: --interval 86400 bot-container` command line tells the Watchtower to check for updates of `bot-container` every 86400 seconds, or 1 time per day.

After all these steps, we are able to launch both container in a background (`-d` flag, detached mode) with this command:
```cmd
docker compose up -d
```

At the moment, we can forget about all manual work we did before and just take pleasure of CI/CD's benefits. Just alter the repository, push to `master`, and all deployment job will be done for you automatically.

# Conclusion

To sum up, I'm over the moon to possess this knowledge and share the information with others. Wish this repository did it's main target to familiarize people with CI/CD basics.

Moreover, I'm completely open to receive useful tips and obtain healthy criticism from other developers. 

## What I've made
- [x] Telegram Bot on Python
- [x] 2 CI pipelines: building & pushing Docker images, testing & linting of Python code
- [x] Pipelines trgger everytime the push or PR on master branch emerge
- [x] Upload Docker Image on Docker Hub
- [x] Rollout of Telegram Bot on Virtual Private Server
- [x] Force Docker container update every time when parent image is updated

The [bot](https://t.me/bigboi666bot) is still rinning and you can play with it whenever you want. Furthermore, if you want to change bot's behaviour, do not be afraid to fork this repository and create a pull request to merge it inside `master` branch.

<img src="https://user-images.githubusercontent.com/46136468/232711246-9e890ed0-5a45-4314-bd67-b0db11a57171.png"  width="75%" height="75%">
