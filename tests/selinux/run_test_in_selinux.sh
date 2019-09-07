#!/bin/sh

installed_plugins="$(vagrant plugin list)"
required_plugins="vagrant-vbguest vagrant-reload"

for plugin in $required_plugins
do
  is_installed=$(echo $installed_plugins | grep $plugin)
  if [ -z "$is_installed" ]; then
    vagrant plugin install $plugin
  else
    echo "$plugin is already installed!"
  fi
done

vagrant up

vagrant ssh <<CMD
sudo setenforce Enforcing
cd /mnt
sudo python3 setup.py install
sudo python3 tests/run_tests.py
CMD

vagrant halt
