from topology import Topology, TestTopology
from mininet.net import Mininet
from minicps.mcps import MiniCPS
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch


def init():
    ## TODO Run init script
    return


def is_initialised():
    ## TODO Check if DB has been set up
    return


class Simulation(MiniCPS):

    def __init__(self, name, net, config):
        self.name = name
        self.net = net

        net.start()

        net.pingAll()

        ## TODO get devives
        ## devices = self.net.get(config.devices)
        ## for device in devices:
        ## device.cmd(f"{sys.executable} -u {config.devices[device].script} &> logs/{config.devices[devices].name}.log &")

        ## TODO start simulation

        CLI(self.net)
        net.stop()


if __name__ == '__main__':
    # if not is_initialised():
    #     init()
    #
    topo = Topology()

    print("Connecting to SDN controller")
    remote_opendaylight = RemoteController('controller_floodlight', "192.168.56.1", port=6653, protocols="OpenFlow13")

    net = Mininet(topo=topo, controller=remote_opendaylight, switch=OVSSwitch)
    net.start()
    print(f"Mininet starting")
    CLI(net)
    net.stop()
    print("Mininet stopping")

