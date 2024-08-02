from pysnmp.hlapi import *
from pysnmp.smi import builder, view, compiler
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher

# Função para verificar se o OID está registrado


def is_oid_registered(mib_view, oid_str):
    try:
        result = mib_view.getNodeName(oid_str)
        return True
    except Exception:
        return False


# Configuração do MIB Builder e Viewer
mib_builder = builder.MibBuilder()
mib_view = view.MibViewController(mib_builder)

# Carregar MIBs
compiler.addMibCompiler(mib_builder, sources=[
                        'http://mibs.snmplabs.com/asn1/@mib@'])
mib_builder.loadModules('SNMPv2-MIB')

# Definindo OID e seu valor
oid_str = '1.3.6.1.2.1.1.1.0'

# Verificação se o OID já está registrado
if not is_oid_registered(mib_view, oid_str):
    print("OID is not registered!")

# Iniciar um transport dispatcher para receber traps
transport_dispatcher = AsyncoreDispatcher()

# Configuração do receptor de trap
transport_dispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode(('0.0.0.0', 162))
)


def cb_fun(transport_dispatcher, transport_domain, transport_address, whole_msg):
    while whole_msg:
        msg_ver = int(api.decodeMessageVersion(whole_msg))
        if msg_ver in api.protoModules:
            p_mod = api.protoModules[msg_ver]
            req_msg, whole_msg = decoder.decode(
                whole_msg, asn1Spec=p_mod.Message(), )
            print('Notification message from %s:%s: ' % (
                transport_domain, transport_address))
            req_pdu = api.getMessageComponent(req_msg, 'pdu')
            print('Notification type: %s' %
                  (p_mod.apiPDU.getCmd(req_pdu).prettyPrint()))
            for oid, val in api.varBinds:
                print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
        else:
            print('Unsupported SNMP version %s' % (msg_ver))
    return whole_msg


transport_dispatcher.registerRecvCbFun(cb_fun)

# Roda o servidor indefinidamente para receber traps
transport_dispatcher.jobStarted(1)
try:
    # Dispatcher will never finish as job#1 never reaches zero
    transport_dispatcher.runDispatcher()
except:
    transport_dispatcher.closeDispatcher()
    raise
