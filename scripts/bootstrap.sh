#!/bin/bash

if [ "$(uname)" == "Darwin" ]; then
  echo "On Mac OS"

  echo "Installing brew"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

  echo "Installing wget"
  brew install wget

  echo "Installing postgresql-14"
  brew install postgresql@14

  echo "Installing python"
  brew install python
  
  echo "Setting up database"
  brew services stop postgresql
  brew services start postgresql
  sleep 3 # sometimes postgresql isn't ready right away
  psql postgres -c "CREATE DATABASE minicorn_db;"
  psql postgres -c "CREATE USER minicorn WITH PASSWORD 'password';"
  psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE minicorn_db TO minicorn;"


elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  echo "On Linux platform"

  if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
  fi

  echo "Installing postgresql-14"
  sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
  wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
  sudo apt-get update
  sudo apt-get -y install postgresql-14

  echo "Installing pyenv and python 3.9"
  if test -f "~/.pyenv"; then
    echo "detecting pyenv already installed"
    apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev\
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl\
    git
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

    # This only works for the default bash shell, otherwise need to copy this over into your own shell config like .zshrc
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
    exec "$SHELL"
  fi

  pyenv install 3.9.6
  pyenv local 3.9.6

  echo "Setting up database"
  sudo -u postgres psql postgres -f ./db_setup.sql


elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
  echo "Windows currently not supported"
  exit 1
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
  echo "Windows currently not supported"
  exit 1
else
  echo "Unknown OS"
  exit 1
fi

# Common setup
echo "Setting up .env file"
cp ./backend/.env.example ./backend/.env

echo "Installing build dependencies"
cd ./frontend && yarn install && cd ..
pip install -r ./requirements.txt
pip install -r ./ml/requirements.txt
