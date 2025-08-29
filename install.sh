#!/bin/bash

set -e

BOT_DIR=~/mybot/currency
REPO_DIR="https://github.com/arvinmoradi/usd_irr_bot.git"

mkdir -p $BOT_DIR

show_menu() {
    clear
    echo "==========================="
    echo "   مدیریت ربات تلگرام"
    echo "==========================="
    echo "1) Install"
    echo "2) Update"
    echo "3) Uninstall"
    ehco "4) Exit"
    echo "==========================="
    read -p "Choose:" choice
}

while True; do
    show_menu
    case $choice in
        1) install_bot ;;
        2) update_bot ;;
        3) uninstall_bot ;;
        4) echo "Exit..."; exit 0 ;;
        *) echo "Invalid Choise"; sleep 2 ;;
    esac
done