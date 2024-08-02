# Busca MIB para a IEE1
# Autor: Mauricio Menon
# Versao 1.1 24/08/2023

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTextBrowser
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity


class SNMPFetcher(QThread):
    fetched = pyqtSignal(str)

    def __init__(self, ip_address, oids):
        super().__init__()
        self.ip_address = ip_address
        self.oids = oids

    def run(self):
        results = []
        for oid, description in self.oids:
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData('public', mpModel=0),
                       UdpTransportTarget((self.ip_address, 161)),
                       ContextData(),
                       ObjectType(ObjectIdentity(oid)))
            )

            if errorIndication:
                results.append(f"{description}: Erro - {errorIndication}")
            elif errorStatus:
                results.append(
                    f"{description}: Erro - {errorStatus.prettyPrint()}")
            else:
                for varBind in varBinds:
                    results.append(f"{description}: {varBind[1]}")

        self.fetched.emit("\n".join(results))


class SNMPTrapApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        layout = QVBoxLayout()

        self.ipAddressInput = QLineEdit("localhost", self)
        self.ipAddressInput.editingFinished.connect(self.clearDefaultIP)
        self.ipAddressInput.setPlaceholderText("Entre o endereço IP")
        layout.addWidget(self.ipAddressInput)

        fetchValuesButton = QPushButton("Buscar valores", self)
        fetchValuesButton.clicked.connect(self.startFetching)
        layout.addWidget(fetchValuesButton)

        self.resultBrowser = QTextBrowser(self)
        layout.addWidget(self.resultBrowser)

        self.setLayout(layout)
        self.setWindowTitle('SNMP Value Fetcher')
        self.show()

    def clearDefaultIP(self):
        if self.ipAddressInput.text() == "localhost":
            self.ipAddressInput.clear()

    def startFetching(self):
        self.resultBrowser.setPlainText("Buscando valores... Aguarde.")
        QTimer.singleShot(100, self.fetchValues)

    def fetchValues(self):
        ip_address = self.ipAddressInput.text()

        oids = [
            ('.1.3.6.1.4.1.31823.1.3500.1.1.1.0', "CPU Burden"),
            ('.1.3.6.1.4.1.31823.1.3500.1.1.2.0', "Memory Used (kB)"),
            ('.1.3.6.1.4.1.31823.1.3500.1.1.3.0', "Mainboard Temperature (C)")
        ]

        self.fetcher = SNMPFetcher(ip_address, oids)
        self.fetcher.fetched.connect(self.displayResults)
        self.fetcher.start()

    def displayResults(self, result):
        self.resultBrowser.setPlainText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SNMPTrapApp()
    sys.exit(app.exec())
