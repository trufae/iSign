#!/bin/bash

# Colors
RED='\033[0;31m'
WHITE='\033[1;37m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${RED}Setup iSign Linux${NC}"

# Install requeriments and iSign
function start_install() {
    echo -e "${WHITE}Installing Python Setup tools"
    apt-get -qq --assume-yes install python-setuptools
    apt-get -qq --assume-yes install zip
    apt-get -qq --assume-yes install curl
    apt-get -qq --assume-yes install git
    easy_install pip
    echo -e "${WHITE}Fix OpenSSH bug"
    sudo rm -rf /usr/local/lib/python2.7/dist-packages/OpenSSL/
    apt-get -qq --assume-yes install --reinstall python-openssl
    echo -e "${WHITE}Installing iSign"
    #git clone https://github.com/involvestecnologia/iSign.git
    cd ../isign/
    chmod +x INSTALL.sh
    ./INSTALL.sh 
}

# Remove setuptools, zip, curl and openSSL
function start_uninstall() {
    pip uninstall isign
    pip uninstall pip
    apt-get -qq --assume-yes remove python-setuptools
    apt-get -qq --assume-yes remove zip
    apt-get -qq --assume-yes remove curl
    apt-get -qq --assume-yes remove git
    apt-get -qq --assume-yes remove python-openssl
    sudo rm -rf /usr/local/lib/python2.7/dist-packages/OpenSSL/
}

# Download Apple Certificates
function certificates(){
    echo "Downloading Apple Certificates"
    curl 'https://www.apple.com/appleca/AppleIncRootCertificate.cer' > AppleIncRootCertificate.cer
    curl 'https://developer.apple.com/certificationauthority/AppleWWDRCA.cer' > AppleWWDRCA.cer
    echo "Importing..."
    openssl x509 -inform der -in AppleIncRootCertificate.cer -outform pem -out AppleIncRootCertificate.pem
    openssl x509 -inform der -in AppleWWDRCA.cer -outform pem -out AppleWWDRCA.pem
    echo "Generating applecerts.pem" 
    cat AppleWWDRCA.pem AppleIncRootCertificate.pem > applecerts.pem
}

# Check if sudo
ROOT_UID=0
if [ $UID != $ROOT_UID ]; then
    echo -e "${RED}/!\ ${NC}You don't have sufficient privileges to run this script.${NC}"
    exit 1
fi

# Check if distro is Debian based
APT_GET_CMD=$(which apt-get)
if [[ ! -z $APT_GET_CMD ]]; then
    if [ "$1" == "install" ]; then
    start_install
        certificates
    elif [ "$1" == "uninstall" ]; then
        start_uninstall
    elif [ "$1" == "certificates" ]; then
        certificates
    else
        echo "too few arguments" 
    fi
else
    echo -e "${RED}/!\ ${NC}This script require a distro Debian based.${NC}"
    exit 1
fi
