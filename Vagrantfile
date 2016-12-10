# -*- mode: ruby -*-
# vi: set ft=ruby :

PROJECT = "django-test"
BRANCH = "deployment-script-test"
REPOSITORY = "https://github.com/TeaTracer/#{PROJECT}.git"

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/trusty64"

    config.vm.define "prod" do |prod|
        config.vm.network "forwarded_port", guest: 80, host: 1234, auto_correct: true
        config.vm.provider "virtualbox" do |vb|
            vb.gui = false
            vb.name = "prod"
            vb.memory = "1024"
            vb.cpus = "4"
        end
        config.vm.provision "shell", inline: "sudo hostnamectl set-hostname prod"
        config.vm.provision "shell", path: "deploy_to_server.sh"
    end

    config.vm.define "dev" do |dev|
        config.vm.network "forwarded_port", guest: 80, host: 1235, auto_correct: true
        config.vm.provider "virtualbox" do |vb|
            vb.gui = false
            vb.name = "dev"
            vb.memory = "512"
            vb.cpus = "2"
        end
        config.vm.provision "shell", inline: "sudo hostnamectl set-hostname dev"
        config.vm.provision "shell", path: "deploy_to_server.sh"
    end
end
