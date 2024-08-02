from pysnmp.hlapi import *

def get_snmp_data(target_ip, oid_list):
    data = {}

    for oid in oid_list:
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData('public', mpModel=0),
                   UdpTransportTarget((target_ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid)))
        )

        if errorIndication:
            print(errorIndication)
            return None
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            return None
        else:
            for varBind in varBinds:
                data[oid] = varBind[1].prettyPrint()

    return data

if __name__ == "__main__":
    oids = [
        '.1.3.6.1.4.1.31823.1.3500.1.1.1.0',  # CPU Burden
        '.1.3.6.1.4.1.31823.1.3500.1.1.2.0',  # Memory Used (kB)
        '.1.3.6.1.4.1.31823.1.3500.1.1.3.0'   # Mainboard Temperature (°C)
    ]

    results = get_snmp_data('127.0.0.1', oids)
    
    if results:
        print("CPU Burden: %s%%" % results[oids[0]])
        print("Memory Used: %s kB" % results[oids[1]])
        print("Mainboard Temperature: %s°C" % results[oids[2]])
