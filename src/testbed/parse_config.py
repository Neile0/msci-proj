import pprint
import sys
import xmltodict

_LINKS = []
_DEVICES = []
_SWITCHES = []


def get_file():
    args = sys.argv
    if not len(args) > 1:
        print("Provide topology file as an argument")
        return
    return sys.argv[1]


def process_device(device):
    print(f"Device: {device['Id']}")
    _DEVICES.append(device['Id'])

    if 'Links' in device.keys():
       process_links(device, device['Links'])
    return


def process_device_group(device_group):
    print(f"Device Group {device_group['Name']}")

    for device in device_group['Device']:
        process_device(device)
    return


def get_device_count(devices):
    print(type(devices))
    pprint.pprint(devices)
    if "Devices" not in devices.keys():
        return 1

    # device_array = devices['Device']
    # print(type(device_array))
    return


def process_link(link_from, link_to):
    _link_to = link_to['@To']
    if (link_from, _link_to) not in _LINKS and (_link_to, link_from) not in _LINKS:
        print(f"Adding Link: {link_from} -> {_link_to}")
        _LINKS.append((link_from, _link_to))
    return

def process_links(device_from, links):
    _links = links['Link']
    if type(_links) is list:
        for link in _links:
            process_link(device_from['Id'], link)
    else:
        process_link(device_from['Id'], _links)

def process_switch(switch):
    print(f"Switch {switch['Id']}")
    _SWITCHES.append(switch['Id'])
    if 'Links' in switch.keys():
        process_links(switch, switch['Links'])

def process_network_section(section):
    print(f"Section - {section['Name']} ({section['Id']})")
    print()
    print("Switches")
    switches = section['Switch']
    # pprint.pprint(switches)
    # print(type(switches))
    if type(switches) is list:
        for switch in switches:
            process_switch(switch)
    else:
        process_switch(switches)


    print()
    print("Devices")


    devices_collection = section['Devices']
    if 'DeviceGroup' in devices_collection.keys():
        device_groups = devices_collection['DeviceGroup']
        if type(device_groups) is list:
            for device_group in device_groups:
                process_device_group(device_group)
        else:
            process_device_group(device_groups)
        pass

    if 'Device' in devices_collection.keys():
        devices = devices_collection['Device']
        if type(devices) is list:
            for device in devices:
                process_device(device)
        else:
            process_device(devices)

    print('-' * 50)
    return


def parse_config():
    file_name = get_file()
    if file_name is None:
        return

    with open(file_name, 'r', encoding='utf-8') as file:
        xml = file.read()

    config = xmltodict.parse(xml)["Network"]

    network_name = config["Name"]

    print("-" * 50)
    print(f"Topology provided by: {file_name}")
    print(f"Network - {network_name}")
    print("-" * 50)

    sections = config[("NetworkSection")]
    for section in sections:
        process_network_section(section)

    print("Network Parsed")
    return {'Devices': _DEVICES,'Switches': _SWITCHES, 'Links': _LINKS }


if __name__ == '__main__':
    parse_config()
