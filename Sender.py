from abc import ABC, abstractmethod
from pyModbusTCP.client import ModbusClient


class Sender(ABC):
    # Sender é uma classe abstrata que herda de ABC

    @abstractmethod
    def send_signal(self, type: bool):
        # Método abstrato que deve ser implementado pelas subclasses
        pass

    @abstractmethod
    def get_connection(self):
        # Outro método abstrato
        pass

    @abstractmethod
    def get_status_machine(self, is_connected: bool):
        # Mais um método abstrato
        pass


class MqttSender(Sender):
    # MqttSender herda de Sender e deve implementar todos os métodos abstratos

    def __init__(self):
        self._is_connected = False
    
    def send_signal(self, type: bool):
        # Implementação do método abstrato
        print(f"MQTT Signal sent: {type}")

    def get_connection(self):
        # Implementação do método abstrato
        print("MQTT connection established")

    def get_status_machine(self, is_connected: bool):
        # Implementação do método abstrato
        self._is_connected = is_connected
        return self._is_connected


class ModBusSender(Sender):
    def __init__(self, ip, port, slave_address):
        self._client = ModbusClient(host=ip, port=port, unit_id=slave_address)
        self._is_connected = False

    def send_signal(self, type_signal: bool):
        signal_value = 1 if type_signal else 0
        if self._client.write_single_register(1, 1):
            print(f"ModBus Signal sent: {type_signal}")
        else:
            print("Failed to send ModBus Signal")

    def get_connection(self):
        try:
            self._is_connected = self._client.open()
            if self._is_connected:
                print("ModBus connection established")
            else:
                print("Failed to establish connection")
        except Exception as e:
            print(f"Failed to establish connection: {e}")
            self._is_connected = False

    def get_status_machine(self, is_connected: bool):
        self._is_connected = is_connected
        status = self._client.read_holding_registers(2, 1)
        if status:
            return status[0]
        else:
            print("Failed to read status register")
            return None





