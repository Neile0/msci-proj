
Vagrant.configure("2") do |config|
    # For a complete reference, please see the online documentation at
    # https://docs.vagrantup.com.

#     config.vm.provider "virtualbox" do |vb|
#         vb.customize ["modifyvm", :id, "--nic2", "hostonly", "--hostonlyadapter2", "VirtualBox Host-Only Ethernet Adapter"]
#         vb.customize ["modifyvm", :id, "--nic3", "natnetwork"]
#         vb.customize ["modifyvm", :id, "--nat-network3", "NatNetwork"]
#     end

    config.vm.box = "ubuntu/focal64"
    config.ssh.forward_agent = true
    config.ssh.forward_x11 = true

    config.vm.define "controller" do |controller|
        controller.vm.hostname = "controller"
        controller.vm.network "public_network", ip: "192.168.56.1"
        controller.vm.provision "shell",  path: "bootstrap/bootstrap.controller.sh"
    end

    config.vm.define "testbed" do |testbed|
        testbed.vm.hostname = "testbed"
        testbed.vm.network "public_network", ip: "192.168.56.2"
        testbed.vm.provision "shell", path: "bootstrap/bootstrap.testbed.sh"
    end


    config.vm.define "other" do |other|
        other.vm.hostname = "other"
        other.vm.network "public_network", ip: "192.168.56.3"
    end
end