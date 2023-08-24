from pysnmp.hlapi import *
from pysnmp.smi import view

# Função para converter string OID para tupla


def oid_str_to_tuple(oid_str):
    return tuple(map(int, oid_str.split('.')))

# Função para verificar se o OID está registrado


def is_oid_registered(mib_view, oid_str):
    oid_tuple = oid_str_to_tuple(oid_str)
    try:
        result = mib_view.getNodeName(oid_tuple)
        return result is not None
    except Exception:
        return False


# Criação de um engine SNMP
snmp_engine = SnmpEngine()

# Criação do MibViewController
mib_view = view.MibViewController(snmp_engine.getMibBuilder())

# Configuração do receptor de trap (Estou ignorando essa parte porque não estamos configurando traps aqui)
# trap_receiver = TrapReceiver(snmp_engine, ('0.0.0.0', 162))

# Definindo OID e seu valor
oid_str = '1.3.6.1.2.1.1.1.0'

# Verificação se o OID já está registrado
if not is_oid_registered(mib_view, oid_str):
    snmp_engine.getMibBuilder().importSymbols('SNMPv2-MIB', 'sysDescr')
    snmp_engine.getMibBuilder().defineScalar(
        oid_str_to_tuple(oid_str), Integer32(), maxAccess="readwrite")

# Roda o servidor indefinidamente para receber traps (ignorado pois não foi mostrado como fazer isso com pysnmp)
# trap_receiver.run_forever()
