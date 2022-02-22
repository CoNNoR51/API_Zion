from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."

    # def build(self, n=2):
    #     switch = self.addSwitch('s1')
    #     # Python's range(N) generates 0..N-1
    #     for h in range(n):
    #         host = self.addHost('h%s' % (h + 1))
    #         self.addLink(host, switch)


def simple_test(id, loss, delay):
    "Create and test a simple network"
    topo = SingleSwitchTopo()
    net = Mininet(topo=topo, build=False)
    switch = net.addSwitch('s1', params2={'ip': '172.16.0.1/12'})
    host = net.addHost('h' + str(id))
    host1 = net.addHost('h1')
    net.addLink(host, switch, delay=delay, loss=loss)
    net.addLink(host1, switch)
    c0 = net.addController('c0')
    cmap = {'s1': c0}
    net.build()
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()

    # net.host.
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simple_test()
