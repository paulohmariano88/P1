# import asyncio
# from pymodbus.server import StartTcpServer
# from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
# import logging

# class ModbusServer:

#     def __init__(self):
#         logging.basicConfig(level=logging.INFO)
        
#         # Inicializa os blocos de dados Modbus
#         self.store = ModbusSlaveContext(
#             di=ModbusSequentialDataBlock(0, [0] * 100),  # Discrete Inputs
#             co=ModbusSequentialDataBlock(0, [0] * 100),  # Coils
#             hr=ModbusSequentialDataBlock(0, [0] * 100),  # Holding Registers
#             ir=ModbusSequentialDataBlock(0, [0] * 100),  # Input Registers
#         )
#         self.context = ModbusServerContext(slaves=self.store, single=True)

#     def update_register(self, signal):
#         """Atualiza o valor do registro Modbus"""
#         slave_id = 0x00  # ID do escravo
#         address = 0  # Endereço do registro
#         value = 1 if signal else 0  # Alerta ou Normal
        
#         self.context[slave_id].setValues(3, address, [value])
#         print(value)

#     def run(self, host='0.0.0.0', port=502):
#         """Inicia o servidor Modbus TCP"""
#         logging.info(f"Servidor Modbus rodando em {host}:{port}...")
#         StartTcpServer(context=self.context, address=(host, port))


