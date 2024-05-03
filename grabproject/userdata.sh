#!/bin/bash
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo systemctl restart sshd
sudo yum install httpd -y
sudo systemctl enable httpd --now
sudo useradd your_user_name
echo 'your_user_name:password_you_want_to_give' | sudo chpasswd
echo 'your_user_name  ALL=(ALL) NOPASSWD: ALL' | sudo EDITOR='tee -a' visudo

