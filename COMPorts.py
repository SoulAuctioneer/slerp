import serial.tools.list_ports

def get_com_ports():
    ports = []
    portList = list(serial.tools.list_ports.comports())

    for portFound in portList:
        port = Port(data=dict({"device": portFound.device, "description": portFound.description.split("(")[0].strip()}))
        ports.append(port)

    return ports

def get_description_by_device(device: str):
    for port in get_com_ports():
        if port.device == device:
            return port.description

def get_device_by_description(description: str):
    for port in get_com_ports():
        if port.description == description:
            return port.device

def print_ports():
    ports = get_com_ports()
    for port in ports:
        print(port.device)
        print(port.description)


class Port:
    def __init__(self, data: dict):
        self.data = data
        self.device = data.get("device")
        self.description = data.get("description")
