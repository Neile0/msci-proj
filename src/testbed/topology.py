from mininet.topo import Topo
from src.testbed.parse_config import parse_config


class ICSTopo(Topo):
    def __init__(self, name, devices, switches, links, *args, **params):
        self.name = name
        self.provided_devices = devices
        self.provided_switches = switches
        self.provided_links = links
        super().__init__(*args, **params)

    def build(self):
        for device in self.provided_devices:
            self.addHost(device)

        for switch in self.provided_switches:
            self.addSwitch(switch, protocols='OpenFlow13')

        for link in self.provided_links:
            self.addLink(link[0], link[1])

    def __str__(self):
        string = f"Name: {self.name} | Devices {len(self.provided_devices)} | Switches: {len(self.provided_switches)} | Links: {len(self.provided_links)}"
        return string


class ICSTopoBuilder:

    def __init__(self):
        self.name = "ICS Topo"
        self.devices = []
        self.switches = []
        self.links = set()

    def set_name(self, name):
        self.name = name

    def add_device(self, name):
        if name not in self.devices:
            self.devices.append(name)
        else:
            print("Cannot add duplicate device")

    def add_switch(self, name):
        if name not in self.switches:
            self.switches.append(name)
        else:
            print("Cannot add duplicate switch")

    def add_link(self, deviceFrom, deviceTo):
        if deviceFrom not in self.devices and deviceFrom not in self.switches:
            print(f"Cannot add link for device {deviceFrom} that does not exist")

        if deviceTo not in self.devices and deviceTo not in self.switches:
            print(f"Cannot add link for device {deviceTo} that does not exist")

        if (deviceFrom, deviceTo) not in self.links and (deviceTo, deviceFrom) not in self.links:
            self.links.add((deviceFrom, deviceTo))
        else:
            print(f"Link {deviceFrom} -> {deviceTo} is a duplicate link")

    def build(self):
        topo = ICSTopo(self.name, self.devices, self.switches, self.links)
        return topo


def honeypot_ify(config):
    devices = config['Devices']
    devices_honeyd = []
    for device in devices:
        devices_honeyd.append(device)
        devices_honeyd.append(f"{device}-honey")

    switches = config['Switches']
    switches_honeyd = []
    for switch in switches:
        switches_honeyd.append(switch)
        switches_honeyd.append(f"{switch}-honey")

    links = config['Links']
    links_honeyd = []
    for link in links:
        links_honeyd.append(link)
        continue

    return {'Devices': devices_honeyd, 'Switches': switches_honeyd, 'Links': links_honeyd}


def Topology():
    config = parse_config()
    print("Adding Honeypots")
    config = honeypot_ify(config)
    print("Honeyfied")

    builder = ICSTopoBuilder()
    for device in config['Devices']:
        builder.add_device(device)

    for switch in config['Switches']:
        builder.add_switch(switch)

    for link in config['Links']:
        builder.add_link(link[0], link[1])

    topo = builder.build()
    return topo


class TestTopology(Topo):

    def build(self):
        switch = self.addSwitch('s1', protocols='OpenFlow13')
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')

        self.addLink(host1, switch)
        self.addLink(host2, switch)
        self.addLink(host2, host3)