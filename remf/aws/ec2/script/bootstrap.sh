#!/bin/sh

# ${VAR_PORT_SSH}

# #################################
# Modificando a porta do SSH

sed -i s/"#Port 22"/"Port ${VAR_PORT_SSH}"/g /etc/ssh/sshd_config
sudo systemctl reload sshd
# semanage port -a -t ssh_port_t -p tcp ${VAR_PORT_SSH}
# firewall-cmd --zone=public --add-port=${VAR_PORT_SSH}/tcp --permanent
# firewall-cmd --reload

# #################################
# Diretório /remf

if [ ! -d "${VAR_DIR_CLOUDOPSS}" ]; then
    mkdir ${VAR_DIR_CLOUDOPSS}
fi

echo '# Port SSH: ${VAR_PORT_SSH}
#
#' > ${VAR_DIR_CLOUDOPSS}/.env
