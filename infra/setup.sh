#!/bin/bash

set -e  # Остановить выполнение скрипта при ошибке

cd ./infra;
chmod +x ./install_node.sh;
./install_node.sh;
