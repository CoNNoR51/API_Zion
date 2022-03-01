from mininet.link import TCLink
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


def start(id, net):
    """Creating start net"""
    switch = net.addSwitch('s1')
    switch.configDefault(action='NORMAL')

    host1 = net.addHost('h1', ip='10.0.0.1')
    host2 = net.addHost('h2', ip='10.0.0.3')
    c0 = net.addController('c0')
    cmap = {'s1': c0}

    net.addLink(host1, switch, loss=0, delay='2ms')
    net.addLink(host2, switch, loss=0, delay='2ms')

    net.build()
    net.start()


def host_up_mn(net, id):
    switch = net.get('s1')

    host = net.addHost('h' + str(id), ip='10.0.0.2')
    net.addLink(host, switch)
    switch.setHostRoute('10.0.0.2', 'eth3')
    switch.attach('eth3')
    switch.configDefault(action='NORMAL')
    print(switch.intfList())


    net.build()

    dumpNodeConnections(net.hosts)
    # net.pingAll()


def host_down_mn(net, id):

    net.delLinkBetween(net.get('h' + str(id)), net.get('s1'), allLinks=True)
    net.delHost(net.get('h' + str(id)))

    net.build()


def link_change_mn(net, id, loss, delay):
    """Change loss & delay between userHost and towerHost (h1)"""

    net.delLinkBetween(net.get('h' + str(id)), net.get('s1'), allLinks=True)
    net.addLink(net.get('h' + str(id)), net.get('s1'),
                loss=loss, delay=delay)

    # net.delLinkBetween(net.get('h2'), net.get('s1'), allLinks=True)
    # net.addLink(net.get('h2'), net.get('s1'), loss=loss, delay=delay)

    net.build()


def get_speed_mn(net, id):
    buf = ''
    write = False

    host = net.get('h' + str(id))
    # host = net.get('h2')

    result = host.cmd('ping -c 1 -q 10.0.0.1')
    print(result)

    for char in result:
        if char == '/':
            write = False

        if write:
            buf += char

        if char == '=':
            write = True

    print(buf)

    if buf == '':
        speed = 0
    else:
        time_for_pkg = float(buf)
        print(buf)
        speed = 0.4375 / (time_for_pkg / 1000)

    print('speed = ' + str(speed) + ' Kbit/s')

    return speed


def net_ping_test():
    # topo = SingleSwitchTopo()
    net = Mininet(link=TCLink, build=False)

    switch = net.addSwitch('s1')

    host1 = net.addHost('h1', ip='10.0.0.1')
    host = net.addHost('h2', ip='10.0.0.2')
    c0 = net.addController('c0')
    cmap = {'s1': c0}

    net.addLink(host, switch, delay='90ms')
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
