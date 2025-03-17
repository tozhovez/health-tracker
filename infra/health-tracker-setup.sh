#!/bin/bash

set -e  # Остановить выполнение скрипта при ошибке
# Color variables for better readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

FRONTEND_DIR="frontend/dashboard"


# Обновление списка пакетов
sudo apt update -y && sudo apt upgrade -y

# Установка необходимых зависимостей
sudo apt install -y curl ca-certificates


echo_info() {
  echo -e "${BLUE}[INFO] $1${NC}"
}

echo_success() {
  echo -e "${GREEN}[SUCCESS] $1${NC}"
}

echo_warning() {
  echo -e "${YELLOW}[WARNING] $1${NC}"
}

echo_error() {
  echo -e "${RED}[ERROR] $1${NC}"
  exit 1
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
  echo_error "Node.js is not installed. Please install Node.js first."
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
  echo_error "npm is not installed. Please install npm first."
fi

# Check if Vue CLI is installed
if ! command -v vue &> /dev/null; then
  echo_info "Vue CLI is not installed. Installing Vue CLI..."
  npm install -g @vue/cli
  if [ $? -ne 0 ]; then
    echo_error "Failed to install Vue CLI. Please check your npm configuration."
  fi
  echo_success "Vue CLI installed successfully."
fi
cd dashboard
  npm install
  npm run format
  npm run dev



