# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/trusty64"

    config.vm.define "prod" do |prod|
        config.vm.network "forwarded_port", guest: 8000, host: 1234, auto_correct: true
        config.vm.provider "virtualbox" do |vb|
            vb.gui = false
            vb.name = "prod"
            vb.memory = "512"
            vb.cpus = "2"
        end
        config.vm.provision "shell",  inline: "sudo hostnamectl set-hostname prod"
    end

    config.vm.define "dev" do |dev|
        config.vm.network "forwarded_port", guest: 8000, host: 1235, auto_correct: true
        config.vm.provider "virtualbox" do |vb|
            vb.gui = false
            vb.name = "dev"
            vb.memory = "512"
            vb.cpus = "2"
        end
        config.vm.provision "shell",  inline: "sudo hostnamectl set-hostname dev"
    end
end
