#!/bin/bash

set -e
FRONTEND_DIR="frontend/dashboard"

sudo apt update -y
sudo apt upgrade -y


sudo apt install -y curl ca-certificates



# Проверка установленной версии Node.js и npm
echo "Node.js: $(node -v)"
echo "";
echo "npm : $(npm -v)"
echo "";
#echo "===================================================================================";
#echo "";
#echo "Установка yarn";
#echo "";
#echo "===================================================================================";
#echo "";
## Установка yarn (по желанию)
#if ! command -v yarn &> /dev/null; then
#    echo "Установка Yarn..."
#    npm install -g yarn
#    echo "Yarn версия: $(yarn -v)"
#else
#    echo "Yarn уже установлен."
#fi
#
#
#echo "";
#echo "===================================================================================";
#echo "";
## Проверка работоспособности Node.js
#node -e "console.log('Node.js успешно установлен и работает!')"
#echo "";
#echo "===================================================================================";
#echo "";
#echo "Node.js и npm успешно установлены!"
#echo "";
#echo "===================================================================================";
#echo "";
## Проверка работоспособности Node.js
#node -e "console.log('Node.js успешно установлен и работает!')"
echo "Проверка установленной версии Node.js и npm..."
node -v;
npm -v;
exit();
echo "Установка Vue CLI..."
npm install -g @vue/cli;

echo "Проверка установленной версии Vue CLI..."
vue --version;
echo "Создание директории проекта..."
FRONTEND_DIR="frontend/dashboard"
mkdir -p $FRONTEND_DIR;
cd $FRONTEND_DIR;

echo "Создание нового Vue.js проекта..."
vue create . --default --force;

echo "Установка зависимостей..."
npm install;

echo "Запуск сервера разработки Vue.js..."
npm run dev;

echo "";
echo "===================================================================================";
echo "";
echo "Vue CLI версия: $(vue --version)";
echo "";
echo "===================================================================================";
echo "";
echo "";
echo "===================================================================================";
echo "";
echo "Node.js, npm и Vue.js успешно установлены и запущены!"
echo "";
echo "===================================================================================";
echo "";
