#!/bin/bash

set -e

#-------------- DIR ----------
BOT_DIR="$HOME/usd_irr_arm"
REPO_DIR="https://github.com/arvinmoradi/usd_irr_bot.git"
TEMP_DIR="${BOT_DIR}_temp"
mkdir -p "$BOT_DIR"
mkdir -p "$(dirname "$TEMP_DIR")"


#------ COLORS -------
GREEN='\e[32m'
RED='\e[31m'
YELLOW='\e[33m'
BLUE='\e[34m'
PURPLE='\e[35m'
TURQUOISE='\e[36m'
WHITE='\e[37m'
MAGNETA='\e[35m'
NC='\e[39m'

#-------------- O.VARIABLES ----------
SERVICE_NAME="arm_currency_bot.service"
VERSION="v0.1.0"

#---------------FUNCTIONS--------------
check_status() {
    if [ -d "$BOT_DIR" ] && [ -d "$BOT_DIR/venv" ] && [ -d "$BOT_DIR/.git" ]; then
        return 0
    else
        return 1
    fi
}

show_menu() {
    clear
    echo -e "${MAGNETA}===========================${NC}"
    echo -e "${GREEN}Manage Telegram Bot For USD TO IRT${NC}"
    echo -e "${PURPLE}Created By ${BLUE}ArM${NC}"
    echo -e "${BLUE}Telegram: ${YELLOW}@ArvinMoradi${NC}"
    echo -e "${TURQUOISE}Status: ${status:-${RED}NOT INSTALLED${NC}}"
    echo -e "Version: $VERSION"
    echo -e "${MAGNETA}===========================${NC}"
    echo -e "${YELLOW}1) Install"
    echo -e "2) Update"
    echo -e "3) Set Cronjob"
    echo -e "4) Uninstall"
    echo -e "5) Exit"
    echo -e "${MAGNETA}===========================${NC}"
    read -p "Choose: " choice
}

install_bot() {
    sudo apt update -y
    sudo apt install -y python3 python3-venv python3-pip git

    if [ -d "$BOT_DIR" ] && [ ! -d "$BOT_DIR/venv" ]; then
        echo -e "❌ ${RED}Directory $BOT_DIR already exists. If you want to reinstall, please uninstall first.${NC}"
        read -p "Press enter to return to main menu...: "
        return
    fi

    if [ ! -d "$BOT_DIR" ]; then
        echo "📦 Cloning bot into $BOT_DIR..."
        git clone "$REPO_DIR" "$BOT_DIR" || { echo "❌ Clone failed"; exit 1; }
        echo -e "🟢 ${BLUE}Installing...${NC}"
    fi

    cd "$BOT_DIR"

    if [ ! -d 'venv' ]; then
        echo -e "${BLUE}Create Virtual Environment...${NC}"
        python3 -m venv venv
    fi

    source venv/bin/activate

    echo -e "${BLUE}Installing dependency...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt

    echo -e "⚙️ ${BLUE}Creating systemd service...${NC}"
    SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Telegram Currency Bot
After=network.target

[Service]
User=root
WorkingDirectory=$BOT_DIR
ExecStart=$BOT_DIR/venv/bin/python3 $BOT_DIR/main.py
Restart=always
RestartSec=10
Environment=API_TOKEN=$API_TOKEN
Environment=NOBITEX_TOKEN=$NOBITEX_TOKEN
Environment=CHANNEL_ID=$CHANNEL_ID
Environment=CHANNEL_ID_2=$CHANNEL_ID_2

[Install]
WantedBy=multi-user.target
EOF

    sudo sed -i 's/^[[:space:]]*//' $SERVICE_FILE
    echo "🔹 Enabling and starting service..."
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_NAME}
    sudo systemctl start ${SERVICE_NAME}

    echo -e "✅ ${GREEN}Bot installed and service created successfully!${NC}"
    deactivate
    status="${GREEN}INSTALLED${NC}"
    read -p 'press key to back main menu: '
}

update_bot() {
    if check_status; then
        echo -e "🚀 ${BLUE}Installing bot...${NC}"
        cd "$BOT_DIR"
        source venv/bin/activate
        git pull origin main
        pip install --upgrade -r requirements.txt
        deactivate
        sudo systemctl restart $SERVICE_NAME
        echo "✅ Update completed!"
    else
        read -p "❌ Bot not installed. Do you want to install it now? (y/n): " ans
        if [[ "$ans" == "y" || "$ans" == 'Y' ]]; then
            install_bot
        fi
    fi
    read -p 'press key to back main menu: '
}

set_cronjob() {
    if ! check_status; then
        read -p "❌ Bot not installed. Do you want to install it now? (y/n): " ans
        if [[ $ans == "y" || $ans == "Y" ]]; then
            install_bot
        else
            show_menu
        fi
    fi

    while true; do
        clear
        echo -e "${MAGNETA}===========================${NC}"
        echo -e "${GREEN}Add Cronjob${NC}"
        echo -e "${MAGNETA}===========================${NC}"
        echo -e "${YELLOW}1) 30 Min"
        echo -e "2) 1 Hour"
        echo -e "3) 2 Hour"
        echo -e "4) 3 Hour"
        echo -e "5) 6 Hour"
        echo -e "6) 12 Hour"
        echo -e "0) Back to main menu"
        echo -e "${MAGNETA}===========================${NC}"
        read -p "Choice: " opt

        crontab -l 2>/dev/null | grep -v "sender.py" | crontab -

        case $opt in
            1) schedule="*/30 * * * *" ;;
            2) schedule="0 */1 * * *" ;;
            3) schedule="0 */2 * * *" ;;
            4) schedule="0 */3 * * *" ;;
            5) schedule="0 */6 * * *" ;;
            6) schedule="0 */12 * * *" ;;
            0) return ;; #main menu
            *) echo "Invalid Choice..."; sleep 2; continue ;;
        esac

        cmd="$schedule $BOT_DIR/venv/bin/python3 $BOT_DIR/sender.py >> $BOT_DIR/cron.log 2>&1"
        (crontab -l 2>/dev/null; grep -v -F "$cmd"; echo "$cmd") | crontab -
        echo "✅ Cronjob Add: $cmd"
        read -p "press key to back main menu..."
    done
}

uninstall_bot() {
    if check_status; then
        echo "🗑 ${BLUE}Uninstalling bot...${NC}"
        sudo systemctl stop $SERVICE_NAME
        sudo systemctl disable $SERVICE_NAME
        sudo rm -f /etc/systemd/system/$SERVICE_NAME
        sudo systemctl daemon-reload
        rm -rf $BOT_DIR
        crontab -l 2>/dev/null | grep -v "sender.py" | crontab -
        echo -e "✅ ${GREEN}Bot completely uninstalled!${NC}"
    else
        echo -e "❌ ${RED}Nothing to uninstall${NC}"
    fi

    status="${RED}NOT INSTALLED${NC}"

    read -p 'press key to back main menu: '
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
