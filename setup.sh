echo Installing dependencies:
sudo apt install python3 python3-pip
sudo pip3 install -r pip_requirements.txt

echo
echo Configuring service:
sudo cp discord.service  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable discord.service
systemctl status discord.service

echo
echo Run this command to start service:
echo sudo systemctl start discord.service

