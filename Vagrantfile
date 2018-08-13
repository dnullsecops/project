disk = '/data/.vagrant/secondHDD.vdi'

Vagrant.configure("2") do |config|
  config.vm.define "arch" do |arch|
    arch.vm.box = "archlinux/archlinux"
    arch.vm.hostname = "arch"
    arch.vm.network "private_network", ip: "10.0.1.101"
    arch.ssh.insert_key = false
    arch.vm.provider :virtualbox do |vb|
        vb.gui = false
        vb.memory = 2048
        vb.cpus = 2
        # vb.customize ['createhd', '--filename', disk, '--variant', 'Fixed', '--size', 5 * 1024] 
        # vb.customize ['storageattach', :id,  '--storagectl', 'IDE', '--port', 2, '--device', 1, '--type', 'hdd', '--medium', disk]
    end
  end
end

Vagrant.configure("2") do |config|
  # config.vm.provision "shell", inline: "sudo dnf install python2 python-simplejson python-dnf libselinux-python -y -q"
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.define "sles12" do |sles12|
    sles12.vm.box = "elastic/sles-12-x86_64"
    sles12.vm.hostname = "sles12"
    sles12.vm.network "private_network", ip: "10.0.1.121"
    sles12.ssh.insert_key = false
  end

  config.vm.define "master" do |master|
    master.vm.box = "fedora/27-cloud-base"
    master.vm.hostname = "master"
    master.vm.network "private_network", ip: "10.0.1.101"
    master.ssh.insert_key = false
  end

  config.vm.define "application" do |application|
    application.vm.box = "fedora/24-cloud-base"
    application.vm.hostname = "application"
    application.vm.network "private_network", ip: "10.0.1.102"
    application.ssh.insert_key = false
  end

  config.vm.define "database" do |database|
    database.vm.box = "suse/sles11sp3"
    database.vm.hostname = "database"
    database.vm.network "private_network", ip: "10.0.1.103"
    database.ssh.insert_key = false
  end

  config.vm.define "archive" do |archive|
    archive.vm.box = "opensuse/openSUSE-15.0-x86_64"
    archive.vm.hostname = "archive"
    archive.vm.network "private_network", ip: "10.0.1.104"
    archive.ssh.insert_key = false
  end

  config.vm.define "ds" do |ds|
    ds.vm.box = "centos/7"
    ds.vm.hostname = "ds"
    ds.vm.network "private_network", ip: "10.0.1.105"
    ds.ssh.insert_key = false
  end

  config.vm.define "auction_database" do |auction_database|
    auction_database.vm.box = "fedora/24-cloud-base"
    auction_database.vm.hostname = "auction-database"
    auction_database.vm.network "private_network", ip: "10.0.1.106"
    auction_database.ssh.insert_key = false
  end

  config.vm.define "auction_worker" do |auction_worker|
    auction_worker.vm.box = "fedora/24-cloud-base"
    auction_worker.vm.hostname = "auction-worker"
    auction_worker.vm.network "private_network", ip: "10.0.1.107"
    auction_worker.ssh.insert_key = false
  end

  config.vm.define "auction_frontend" do |auction_frontend|
    auction_frontend.vm.box = "fedora/24-cloud-base"
    auction_frontend.vm.hostname = "auction-frontend"
    auction_frontend.vm.network "private_network", ip: "10.0.1.108"
    auction_frontend.ssh.insert_key = false
  end

  config.vm.define "edr_proxy" do |edr_proxy|
    edr_proxy.vm.box = "fedora/24-cloud-base"
    edr_proxy.vm.hostname = "edr-proxy"
    edr_proxy.vm.network "private_network", ip: "10.0.1.109"
    edr_proxy.ssh.insert_key = false
  end

  config.vm.define "databridge" do |databridge|
    databridge.vm.box = "fedora/24-cloud-base"
    databridge.vm.hostname = "databridge"
    databridge.vm.network "private_network", ip: "10.0.1.110"
    databridge.ssh.insert_key = false
  end

  config.vm.define "backup" do |backup|
    backup.vm.box = "fedora/24-cloud-base"
    backup.vm.hostname = "backup"
    backup.vm.network "private_network", ip: "10.0.1.111"
    backup.ssh.insert_key = false
  end

  config.vm.define "billing" do |billing|
    billing.vm.box = "fedora/24-cloud-base"
    billing.vm.hostname = "billing"
    billing.vm.network "private_network", ip: "10.0.1.112"
    billing.ssh.insert_key = false
  end

end

