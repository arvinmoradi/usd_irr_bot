#!/bin/bash

set -e

#-------------- DIR ----------
BOT_DIR=$HOME/mybot
REPO_DIR="https://github.com/arvinmoradi/usd_irr_bot.git"
mkdir -p $BOT_DIR

#------ COLORS -------
GREEN='\e[32m'
RED='\e[31m\'
YELLOW='\e[33m'
BLUE='\e[34m'
PURPLE='\e[35m'
TURQUOISE='\e[36m'
WHITE='\e[37m'
NC='\e[30m'

#---------------FUNCTIONS--------------
show_menu() {
    clear
    echo -e "${GREEN}===========================${NC}"
    echo -e "${GREEN}Manage Telegram Bot For USD TO IRT${NC}"
    echo -e "${PURPLE}Created By ${BLUE}ArM${NC}"
    echo -e "${BLUE}Telegram: ${YELLOW}@ArvinMoradi${NC}"
    echo -e "${GREEN}===========================${NC}"
    echo -e "${YELLOW}1) Install"
    echo -e "${YELLOW}2) Update"
    echo -e "${YELLOW}3) Set Cronjob"
    echo -e "${YELLOW}4) Uninstall"
    echo -e "${YELLOW}5) Exit"
    echo -e "${GREEN}==========================="
    read -p "Choose:" choice
}

install_bot() {
    echo "🚀 Installing bot..."
    cd $BOT_DIR

    echo 'Updating...'
    sudo apt update -y
    sudo apt install -y python3 python3-venv python3-pip git

    if [ ! -d '.git' ]; then
        git clone $REPO_DIR .
    else
        git pull origin main
    fi

    if [ ! -d 'venv' ]; then
        echo 'Create Virtual Environment...'
        python3 -m venv venv
    fi

    source venv/bin/activate

    echo 'Installing dependency...'
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo '✅ Install Successfuly'
    deactivate
    read -p 'press key to back main menu: '
}

update_bot() {
    echo -e "🔄 Updating bot..."
    read -p 'press key to back main menu: '
}

uninstall_bot() {
    echo "🗑 Uninstalling bot..."
    read -p 'press key to back main menu: '
}

set_cronjob() {
    clear
    echo "==========================="
    echo "Add Cronjob"
    echo "==========================="
    echo "1) 30 Min"
    echo "2) 1 Hour"
    echo "3) 2 Hour"
    echo "4) 3 Hour"
    echo "5) 6 Hour"
    echo "6) 12 Hour"
    echo "==========================="
    read -p "Choice: " opt

    crontab -l 2>/dev/null | grep -v "sender.py" | crontab -

    case $opt in
        1) schedule="*/30 * * * *" ;;
        2) schedule="0 */1 * * *" ;;
        3) schedule="0 */2 * * *" ;;
        4) schedule="0 */3 * * *" ;;
        5) schedule="0 */6 * * *" ;;
        6) schedule="0 */12 * * *" ;;
        *) echo "Invalid Choice..."; sleep 2; return ;;
    esac

    cmd="$schedule /root/mybot/currency/venv/bin/python3 /root/mybot/currency/sender.py >> /root/mybot/currency/cron.log 2>&1"

    (crontab -l 2>/dev/null; grep -v -F "$cmd"; echo "$cmd") | crontab -

    echo "✅ Cronjob Add: $cmd"
    echo
    read -p "press key to back main menu..."
}

#-----------RUN-------------
while true; do
    show_menu
    case $choice in
        1) install_bot ;;
        2) update_bot ;;
        3) set_cronjob ;;
        4) uninstall_bot ;;
        5) echo "Exit..."; exit 0 ;;
        *) echo "Invalid Choice"; sleep 2 ;;
    esac
done
