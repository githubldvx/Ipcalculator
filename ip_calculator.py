__initial_author__ = 'Kailash Joshi'
__modified_by__ = 'Ludovic Delporte'
import sys

def _dec_to_binary(ip_address):  # for ip_address = [10, 18, 1, 130], return ['00001010', '00010010', '00000001', '10000010']
    return map(lambda x: bin(x)[2:].zfill(8), ip_address)


def _negation_mask(net_mask):  # for net_mask = [255, 255, 252, 0], return wild = [0, 0, 3, 255]
    wild = list()
    for i in net_mask:
        wild.append(255 - int(i))
    return wild


class IPCalculator(object):
    def __init__(self, ip_address, cdir=24):
        if '/' in ip_address:  # s'il trouve un / après l'IP
            self._address_val, self._cidr = ip_address.split('/')  # example : 10.18.1.130/22 => self._address_val = 10.18.1.130 && self._cidr = 22
            _address = map(int, self._address_val.split('.'))  # example : ip_address = 10.18.1.130 => self._address = [10, 18, 1, 130]
            self._address = []
            for elt in _address:
                self._address.append(elt)
        else:
            _address = map(int, ip_address.split('.'))  # example : ip_address = 10.18.1.130 => self._address = [10, 18, 1, 130]
            self._address = []
            for elt in _address:
                self._address.append(elt)
            self._cidr = cdir  # default cdir=24

        binary_IP = _dec_to_binary(self._address)  # example : return ['00001010', '00010010', '00000001', '10000010']
        self.binary_IP = []
        for elt in binary_IP:
            self.binary_IP.append(elt)
        self.binary_Mask = None
        self.negation_Mask = None
        self.network = None
        self.broadcast = None

    def __repr__(self):
        print("Calculating the IP range of %s/%s" % (".".join(map(str, self._address)), self._cidr))
        print("==================================")
        print("Netmask %s" % (".".join(map(str, self.net_mask()))))
        print("Network ID %s" % (".".join(map(str, self.network_ip()))))
        print("Subnet Broadcast address %s" % (".".join(map(str, self.broadcast_ip()))))
        print("Host range %s" % (self.host_range()))
        # print("Max number of hosts %s" % (self.number_of_host()))

    def net_mask(self):  # for a given cidr, return mask. example : cidr = 22, mask = [255, 255, 252, 0]
        mask = [0, 0, 0, 0]
        for i in range(int(self._cidr)):
            mask[int(i / 8)] += 1 << (7 - i % 8)  # voir ci dessous example avec /22
            # mask = [128, 0, 0, 0]
            # mask = [192, 0, 0, 0]
            # mask = [224, 0, 0, 0]
            # mask = [240, 0, 0, 0]
            # mask = [248, 0, 0, 0]
            # mask = [252, 0, 0, 0]
            # mask = [254, 0, 0, 0]
            # mask = [255, 0, 0, 0]
            # mask = [255, 128, 0, 0]
            # mask = [255, 192, 0, 0]
            # mask = [255, 224, 0, 0]
            # mask = [255, 240, 0, 0]
            # mask = [255, 248, 0, 0]
            # mask = [255, 252, 0, 0]
            # mask = [255, 254, 0, 0]
            # mask = [255, 255, 0, 0]
            # mask = [255, 255, 128, 0]
            # mask = [255, 255, 192, 0]
            # mask = [255, 255, 224, 0]
            # mask = [255, 255, 240, 0]
            # mask = [255, 255, 248, 0]
            # mask = [255, 255, 252, 0]
        self.netmask = mask
        self.binary_Mask = _dec_to_binary(mask)
        self.negation_Mask = _dec_to_binary(_negation_mask(mask))
        return mask

    def broadcast_ip(self):  # for given binary_IP && negation_Mask, return broadcast IP = example : [10, 18, 3, 255]
        broadcast = list()
        for x, y in zip(self.binary_IP, self.negation_Mask):
            broadcast.append(int(x, 2) | int(y, 2))
        self.broadcast = broadcast
        return broadcast

    def network_ip(self):  # for given binary_IP && binary_Mask, return network IP = example : [10, 18, 0, 0]
        network = list()
        for x, y in zip(self.binary_IP, self.binary_Mask):
            network.append(int(x, 2) & int(y, 2))
        self.network = network
        return network

    def host_range(self):  # for a network and broadcast addr (map), return host_range. Example : network = [10, 18, 0, 0], broadcast = [10, 18, 3, 255], result = 10.18.0.1 - 10.18.3.254
        min_range = self.network
        min_range[-1] += 1
        max_range = self.broadcast
        max_range[-1] -= 1
        return "%s - %s" % (".".join(map(str, min_range)), ".".join(map(str, max_range)))

    # def number_of_host(self):
    #     return (2 ** sum(map(lambda x: sum(c == '1' for c in x), self.negation_Mask))) - 2


def ip_calculate(ip):
    ip = IPCalculator(ip)
    ip.__repr__()

if __name__ == '__main__':
    ip = sys.argv[1] if len(sys.argv) > 1 else sys.exit(0)
    ip_calculate(ip)
