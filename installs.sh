#!/bin/sh

yum_makecache() {
  tryCnt=0
  until [$tryCnt -ge 5]
  do
    yum makecache && break
    let tryCnt++
    sleep 1
  done
}

if [ -f /etc/centos-release ] || [ -f /etc/redhat-release ]; then
  yum clean all
  yum -y install epel-release
  yum_makecache

  if [ -z "$(yum list installed | grep mariadb)" ]; then
    echo 'Install mariaDB'
    yum -y install mariadb-server
  fi

  if [ -z "$(which easy_install)" ]; then
    echo 'Install easy_install'
    yum -y install python-setuptools
  fi

  if [ -z "$(which pip)" ]; then
    echo 'Install pip'
    easy_install pip
  fi

  pip install -r requirements.txt

else
  echo 'Sorry. codeMarble is only available in centos'
fi
