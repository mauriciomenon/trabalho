import snmpy

# Função para verificar se o OID está registrado


def is_oid_registered(mib_controller, oid_str):
    try:
        result = mib_controller.get(oid_str)
        return result is not None
    except snmpy.NoSuchObjectError:
        return False


# Criação de um engine SNMP
snmp_engine = snmpy.SnmpEngine()

# Configuração do receptor de trap
trap_receiver = snmpy.TrapReceiver(snmp_engine, ('0.0.0.0', 162))

# Definindo OID e seu valor
oid_str = '1.3.6.1.2.1.1.1.0'

# Verificação se o OID já está registrado
if not is_oid_registered(snmp_engine.mib_controller, oid_str):
    snmp_engine.mib_builder.import_symbols('SNMPv2-MIB', 'sysDescr')
    snmp_engine.mib_builder.define_scalar(
        oid_str, snmpy.Integer32(), max_access="readwrite")

# Roda o servidor indefinidamente para receber traps
trap_receiver.run_forever()
