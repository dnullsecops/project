Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: "sudo dnf install python2 python-simplejson python-dnf libselinux-python -y -q"

  config.vm.define "master" do |master|
    master.vm.box = "fedora/24-cloud-base"
    master.vm.hostname = "master"
    master.vm.network "private_network", ip: "10.0.1.101"
  end

  config.vm.define "client" do |client|
    client.vm.box = "fedora/24-cloud-base"
    client.vm.hostname = "client"
    client.vm.network "private_network", ip: "10.0.1.102"
  end
end

