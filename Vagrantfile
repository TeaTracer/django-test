# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "private_network", ip: "10.10.10.10"

  config.vm.define "ubuntu" do |t|
  end

  config.vm.provider "virtualbox" do |vb|
      vb.name = "ubuntu"
      vb.memory = "1024"
      vb.cpus = "2"
  end

  config.vm.provision "shell",  path: "script.sh"

end
