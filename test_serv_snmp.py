from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.proto.api import v2c

snmpEngine = engine.SnmpEngine()

# Transport setup
# UDP over IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openServerMode(('0.0.0.0', 161))
)

# SNMPv2c setup
# SecurityName <-> CommunityName mapping
config.addV1System(snmpEngine, 'my-area', 'public')

# Allow full MIB access for each user at VACM
config.addVacmUser(snmpEngine, 2, 'my-area', 'noAuthNoPriv', (1, 3, 6, 1, 2, 1), (1, 3, 6, 1, 2, 1))

# Create an SNMP context
snmpContext = context.SnmpContext(snmpEngine)

data = {
    (1, 3, 6, 1, 2, 1, 1, 1, 0): v2c.OctetString('CPU Burden'),
    (1, 3, 6, 1, 2, 1, 1, 2, 0): v2c.OctetString('Memory Used (kB)'),
    (1, 3, 6, 1, 2, 1, 1, 3, 0): v2c.OctetString('Mainboard Temperature (°C)')
}

class CustomResponder(cmdrsp.CommandResponderBase):
    cmdName = cmdrsp.GetCommandResponder.cmdName
    
    def handleMgmtOperation(self, snmpEngine, stateReference, contextName,
                            PDU, acInfo):
        varBinds = []
        
        for oid, val in v2c.apiPDU.getVarBinds(PDU):
            if oid in data:
                varBinds.append((oid, data[oid]))
            else:
                varBinds.append((oid, v2c.NoSuchInstance()))
        
        return contextName, PDU, 0, varBinds

cmdrsp.GetCommandResponder(snmpEngine, snmpContext, CustomResponder())

# Run I/O dispatcher which would receive queries and send confirmations
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
