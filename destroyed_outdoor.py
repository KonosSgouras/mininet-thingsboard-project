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
    s2  = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    ap1 = net.addAccessPoint('ap1', cls=OVSKernelAP, ssid='ap1-ssid',
                             channel='1', mode='g', ip='10.0.0.93', position='310.0,332.0,0', range=300)
    ap2 = net.addAccessPoint('ap2', cls=OVSKernelAP, ssid='ap2-ssid',
                             channel='1', mode='g', ip='10.0.0.94', position='1206.0,219.0,0', range=300)
    ap3 = net.addAccessPoint('ap3', cls=OVSKernelAP, ssid='ap3-ssid',
                             channel='1', mode='g', ip='10.0.0.95', position='727.0,553.0,0', range=400)
    ap4 = net.addAccessPoint('ap4', cls=OVSKernelAP, ssid='ap4-ssid',
                             channel='1', mode='g', ip='10.0.0.96', position='121.0,836.0,0', range=300)
    ap6 = net.addAccessPoint('ap6', cls=OVSKernelAP, ssid='ap6-ssid',
                             channel='1', mode='g', ip='10.0.0.98', position='1189.0,663.0,0', range=300)
    ap7 = net.addAccessPoint('ap7', cls=OVSKernelAP, ssid='ap7-ssid',
                             channel='1', mode='g', ip='10.0.0.99', position='1642.0,435.0,0', range=300)

    info( '*** Add hosts/stations\n')
    sta1 = net.addStation('sta1', ip='10.0.0.1',
                           position='651.0,877.0,0', range=50)
    sta2 = net.addStation('sta2', ip='10.0.0.2',
                           position='1718.0,296.0,0', range=50)
    sta3 = net.addStation('sta3', ip='10.0.0.3',
                           position='1113.0,114.0,0', range=50)
    sta4 = net.addStation('sta4', ip='10.0.0.4',
                           position='301.0,421.0,0', range=50)
    sta5 = net.addStation('sta5', ip='10.0.0.5',
                           position='1295.0,725.0,0', range=50)
    sta6 = net.addStation('sta6', ip='10.0.0.6',
                           position='840.0,355.0,0', range=50)
    sta7 = net.addStation('sta7', ip='10.0.0.7',
                           position='127.0,812.0,0', range=50)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info( '*** Add links\n')
    net.addLink(sta2, ap7)
    net.addLink(sta3, ap2)
    net.addLink(ap1, s2)
    net.addLink(ap4, s2)
    net.addLink(s2, ap3)
    net.addLink(s2, ap6)
    net.addLink(s2, ap2)
    net.addLink(s2, ap7)
    net.addLink(sta7, ap4)
    net.addLink(sta4, ap1)
    net.addLink(sta6, ap3)
    net.addLink(sta5, ap6)
    net.addLink(ap3, sta1)

    net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('s2').start([])
    net.get('ap1').start([c0])
    net.get('ap2').start([c0])
    net.get('ap3').start([c0])
    net.get('ap4').start([c0])
    net.get('ap6').start([c0])
    net.get('ap7').start([c0])

    info( '*** Post configure nodes\n')
    ap1.cmd('ifconfig ap1 10.0.0.93')
    ap2.cmd('ifconfig ap2 10.0.0.94')
    ap3.cmd('ifconfig ap3 10.0.0.95')
    ap4.cmd('ifconfig ap4 10.0.0.96')
    ap6.cmd('ifconfig ap6 10.0.0.98')
    ap7.cmd('ifconfig ap7 10.0.0.99')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

