from abc import ABC, abstractmethod
import threading
from pyModbusTCP.client import ModbusClient

from src.service.modbus_server import ModbusServer


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

    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        self._server = ModbusServer()
        threading.Thread(target=self._server.run, daemon=True).start()
        
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ModBusSender, cls).__new__(cls)
                    cls._instance.__init__()
        return cls._instance

    def send_signal(self, type_signal: bool):
        try:
            self._server.update_register(type_signal)
        except(Exception) as e:
            print("Server Problem: ", e)

    def get_connection(self):
        pass

    def get_status_machine(self, is_connected: bool):
        pass





