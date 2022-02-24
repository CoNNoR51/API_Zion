from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."

    def build(self):
        switch = self.addSwitch('s1')
        host = self.addHost('h1', ip='10.0.0.1')
        self.addLink(host, switch)


def start(id, net):
    """Creating start net"""
    switch = net.addSwitch('s1')

    host1 = net.addHost('h1', ip='10.0.0.1')
    host = net.addHost('h' + str(id), ip='10.0.0.2')
    c0 = net.addController('c0')
    cmap = {'s1': c0}

    net.addLink(host1, switch)
    net.addLink(host, switch)

    net.build()
    net.start()
    # print("Dumping host connections")
    # dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()


def link_change(net, id, loss, delay):
    """Change loss & delay between userHost and towerHost (h1)"""

    net.delLinkBetween()





def net_ping_test():
    # topo = SingleSwitchTopo()
    net = Mininet(build=False)

    switch = net.addSwitch('s1')

    host1 = net.addHost('h1', ip='10.0.0.1')
    host = net.addHost('h2', ip='10.0.0.2')
    c0 = net.addController('c0')
    cmap = {'s1': c0}

    net.addLink(host, switch)
    net.addLink(host1, switch)
    net.build()
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()

    h2 = net.get('h2')
    print('+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+')
    result = h2.cmd('ping -c 1 -q 10.0.0.1')

    print(result)

    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    net_ping_test()
