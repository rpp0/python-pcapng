from __future__ import print_function

import logging
import sys
from collections import Counter

from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP

from pcapng import PcapngReader
from pcapng.objects import EnhancedPacket


logger = logging.getLogger('pcapng')
logger.setLevel(logging.INFO)  # Debug will slow things down a lot!

handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter(
    '\033[1;37;40m  %(levelname)s  \033[0m \033[0;32m%(message)s\033[0m')
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == '__main__':
    import sys
    rdr = PcapngReader(sys.stdin)

    ip_src_count = Counter()
    ip_dst_count = Counter()
    ip_src_size = Counter()
    ip_dst_size = Counter()

    tcp_src_count = Counter()
    tcp_dst_count = Counter()
    tcp_src_size = Counter()
    tcp_dst_size = Counter()

    for block in rdr:
        # print(repr(block))

        if isinstance(block, EnhancedPacket):
            assert block._interface.link_type == 1  # must be ethernet!

            decoded = Ether(block.packet_data)
            # print(repr(Ether(block.packet_data))[:400] + '...')

            _pl1 = decoded.payload
            if isinstance(_pl1, IP):
                ip_src_count[_pl1.src] += 1
                ip_dst_count[_pl1.dst] += 1
                ip_src_size[_pl1.src] += block.packet_len
                ip_dst_size[_pl1.dst] += block.packet_len

                _pl2 = _pl1.payload
                if isinstance(_pl2, TCP):
                    _src = '{0}:{1}'.format(_pl1.dst, _pl2.dport)
                    _dst = '{0}:{1}'.format(_pl1.src, _pl2.sport)
                    tcp_src_count[_src] += 1
                    tcp_dst_count[_dst] += 1
                    tcp_src_size[_src] += block.packet_len
                    tcp_dst_size[_dst] += block.packet_len

    # Print report
    # ------------------------------------------------------------

    def _rsic(o):
        return sorted(o.iteritems(), key=lambda x: x[1], reverse=True)

    print('\n\n')

    print('IP Sources (count)')
    print('-' * 60)
    for key, val in _rsic(ip_src_count)[:30]:
        print("{1:15d} {0}".format(key, val))
    print()

    print('IP Sources (size)')
    print('-' * 60)
    for key, val in _rsic(ip_src_size)[:30]:
        print("{1:15d} {0}".format(key, val))
    print()

    print('IP Destinations (count)')
    print('-' * 60)
    for key, val in _rsic(ip_dst_count)[:30]:
        print("{1:15d} {0}".format(key, val))
    print()

    print('IP Destinations (size)')
    print('-' * 60)
    for key, val in _rsic(ip_dst_size)[:30]:
        print("{1:15d} {0}".format(key, val))
    print()

    print('TCP Sources (count)')
    print('-' * 60)
    for key, val in _rsic(tcp_src_count)[:30]:
        print("{1:15d} {0}".format(key, val))
    print()

    print('TCP Sources (size)')
    print('-' * 60)
    for key, val in _rsic(tcp_src_size)[:30]:
        print("{1:15d} {0}".format(key, val))
    print()

    print('TCP Destinations (count)')
    print('-' * 60)
    for key, val in _rsic(tcp_dst_count)[:30]:
        print("{1:15d} {0}".format(key, val))
    print()

    print('TCP Destinations (size)')
    print('-' * 60)
    for key, val in _rsic(tcp_dst_size)[:30]:
        print("{1:15d} {0}".format(key, val))
    print()
