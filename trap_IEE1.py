import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from pysnmp.hlapi import sendNotification, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, NotificationType


class SNMPTrapApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.ipAddressInput = QLineEdit("localhost", self)
        self.ipAddressInput.editingFinished.connect(self.clearDefaultIP)
        self.ipAddressInput.setPlaceholderText("Enter IP Address")
        layout.addWidget(self.ipAddressInput)

        self.cpuBurdenInput = QLineEdit(self)
        self.cpuBurdenInput.setPlaceholderText("Enter CPU Burden (integer32)")
        layout.addWidget(self.cpuBurdenInput)

        self.memoryUsedInput = QLineEdit(self)
        self.memoryUsedInput.setPlaceholderText(
            "Enter Memory Used (kB, integer32)")
        layout.addWidget(self.memoryUsedInput)

        self.temperatureInput = QLineEdit(self)
        self.temperatureInput.setPlaceholderText(
            "Enter Mainboard Temperature (C, integer32)")
        layout.addWidget(self.temperatureInput)

        sendTrapButton = QPushButton("Send Trap", self)
        sendTrapButton.clicked.connect(self.sendTrap)
        layout.addWidget(sendTrapButton)

        self.resultLabel = QLabel(self)
        layout.addWidget(self.resultLabel)

        self.setLayout(layout)
        self.setWindowTitle('SNMP Trap Sender')
        self.show()

    def clearDefaultIP(self):
        if self.ipAddressInput.text() == "localhost":
            self.ipAddressInput.clear()


    def sendTrap(self):
        ip_address = self.ipAddressInput.text()

        try:
            cpu_burden = int(self.cpuBurdenInput.text())
            memory_used = int(self.memoryUsedInput.text())
            mainboard_temp = int(self.temperatureInput.text())
        except ValueError:
            self.resultLabel.setText("Please enter valid numbers for all values.")
            return

        trap_oids_and_values = [
            ('.1.3.6.1.4.1.31823.1.3500.1.1.1.0', cpu_burden, "CPU Burden"),
            ('.1.3.6.1.4.1.31823.1.3500.1.1.2.0', memory_used, "Memory Used (kB)"),
            ('.1.3.6.1.4.1.31823.1.3500.1.1.3.0',
            mainboard_temp, "Mainboard Temperature (C)")
        ]

        results = []

        for oid, value, description in trap_oids_and_values:
            sendNotification(
                SnmpEngine(),
                CommunityData('public', mpModel=0),
                UdpTransportTarget((ip_address, 162)),
                ContextData(),
                'trap',
                NotificationType(ObjectIdentity(oid)).addVarBinds(
                    ObjectType(ObjectIdentity(oid), value))
            )
            results.append(f"{description}: {value}")

        self.resultLabel.setText("\n".join(results))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SNMPTrapApp()
    sys.exit(app.exec())
