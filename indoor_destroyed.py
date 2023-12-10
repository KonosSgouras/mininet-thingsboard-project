#!/usr/bin/python

from mininet.node import Controller,  OVSKernelSwitch
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from subprocess import call


def myNetwork():

    net = Mininet_wifi(topo=None,
                       build=False,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6653)

    info( '*** Add switches/APs\n')
    s1  = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    ap2 = net.addAccessPoint('ap2', cls=OVSKernelAP, ssid='ap2-ssid',
                             channel='1', mode='g', ip='10.0.0.51', position='482.0,319.0,0', range=300)
    ap3 = net.addAccessPoint('ap3', cls=OVSKernelAP, ssid='ap3-ssid',
                             channel='1', mode='g', ip='10.0.0.52', position='751.0,198.0,0', range=200)
    ap4 = net.addAccessPoint('ap4', cls=OVSKernelAP, ssid='ap4-ssid',
                             channel='1', mode='g', ip='10.0.0.53', position='965.0,357.0,0', range=200)

    info( '*** Add hosts/stations\n')
    sta1 = net.addStation('sta1', ip='10.0.0.1',
                           position='315.0,508.0,0', range=50)
    sta2 = net.addStation('sta2', ip='10.0.0.2',
                           position='548.0,421.0,0', range=50)
    sta3 = net.addStation('sta3', ip='10.0.0.3',
                           position='779.0,69.0,0', range=50)
    sta4 = net.addStation('sta4', ip='10.0.0.4',
                           position='894.0,465.0,0', range=50)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info( '*** Add links\n')
    net.addLink(s1, ap2)
    net.addLink(ap2, sta2)
    net.addLink(ap3, sta3)
    net.addLink(s1, ap3)
    net.addLink(s1, ap4)
    net.addLink(ap4, sta4)
    net.addLink(sta1, ap2)

    net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('s1').start([])
    net.get('ap2').start([c0])
    net.get('ap3').start([c0])
    net.get('ap4').start([c0])

    info( '*** Post configure nodes\n')
    ap2.cmd('ifconfig ap2 10.0.0.51')
    ap3.cmd('ifconfig ap3 10.0.0.52')
    ap4.cmd('ifconfig ap4 10.0.0.53')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

