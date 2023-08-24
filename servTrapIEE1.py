from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asyncio.dgram import udp
import asyncio

# Create SNMP engine instance
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('localhost', 161))
)

# SNMPv1 setup

# SecurityName <-> CommunityName mapping.
config.addV1System(snmpEngine, 'my-area', 'public')

# Allow full MIB access for this user / securityModels at VACM
config.addVacmUser(snmpEngine, 1, 'my-area',
                   'noAuthNoPriv', readSubTree=(1, 3, 6))

# Create an SNMP context with default ContextName
snmpContext = context.SnmpContext(snmpEngine)

# --- configure custom SNMP values ---

cpu_burden = 30  # example value, adjust as needed
memory_used = 2048  # example value in kB, adjust as needed
mainboard_temp = 40  # example value in Celsius, adjust as needed

mibInstrumController = cmdrsp.InstrumentationController()
snmpContext.registerContextName(
    '',  # Default SNMP context
    mibInstrumController  # MIB access controller
)

# Register custom OIDs
mibBuilder = snmpContext.getMibInstrum().getMibBuilder()
mibBuilder.loadModules('SNMPv2-MIB')

MibScalar, MibScalarInstance = mibBuilder.importSymbols(
    'SNMPv2-SMI', 'MibScalar', 'MibScalarInstance')
MibScalarInstance(
    MibScalar('.1.3.6.1.4.1.31823.1.3500.1.1.1.0', 0), (1,)).setSyntax(cpu_burden)
MibScalarInstance(
    MibScalar('.1.3.6.1.4.1.31823.1.3500.1.1.2.0', 0), (1,)).setSyntax(memory_used)
MibScalarInstance(MibScalar('.1.3.6.1.4.1.31823.1.3500.1.1.3.0',
                  0), (1,)).setSyntax(mainboard_temp)

# --- end of custom SNMP values configuration ---

# Apps registration
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.SetCommandResponder(snmpEngine, snmpContext)

# Run SNMP engine
loop = asyncio.get_event_loop()
loop.run_until_complete(snmpEngine.transportDispatcher.runDispatcher())
