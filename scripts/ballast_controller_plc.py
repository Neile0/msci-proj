from datetime import time
from src.testbed.utils import PLC_SAMPLES, PLC_PERIOD_SEC

from minicps.devices import PLC

class BallastControllerPLC(PLC):

    def __init__(self, name,protocol,state, tank_name, tank_gauge, plc_addr, tank_levels, input_valve, output_valve, pump):
        super().__init__(name, protocol, state)
        self.name = name
        self.tank_name = tank_name
        self.plc_addr = plc_addr
        self.tank_gauge = tank_gauge
        self.tank_levels = tank_levels
        self.input_valve = input_valve
        self.output_valve = output_valve
        self.pump = pump

    def pre_loop(self, sleep=0.1):
        print(f'DEBUG: {self.name} enters pre_loop')
        time.sleep(sleep)

    def main_loop(self):
        """Ballast Controller PLC main loop.

            - Read Tank Gauge
            - E
            -

        """

        count = 0
        while count <= PLC_SAMPLES:
            print(f"DEBUG: {self.name} enters main-loop")
            tank_level = float(self.get(self.tank_gauge))
            print(f"DEBUG: {self.name} Tank Gauge Level: {self.tank_gauge}")
            self.send(self.tank_gauge, tank_level, self.plc_addr)

            tank_levels = self.tank_levels['HH']
            if tank_level >= tank_levels['HH']:
              print(f"WARNING {self.name}: {self.tank_name} over EXTREME MAX LEVEL (HH): {tank_level} >= {tank_levels['HH']}")


            if tank_level >= tank_levels['H']:
                print(f"INFO {self.name}: {self.tank_name} over MAX LEVEL (H) ->  closing {self.tank_name} input value")
                self.set(self.value, 0)
                self.send(self.valve, 0, self.plc_addr)

            elif tank_level <= tank_levels['LL']:
                print(f"WARNING {self.name}: {self.tank_name} under EXTREME MIN LEVEL (LL): {tank_level} <= {tank_levels['LL']}")


            elif tank_level <= tank_levels['L']:
                print(f"INFO {self.name}: {self.tank_name} under MIN LEVEL (L) -> closing {self.tank_name} output value, shutting off {self.tank_name} pump")
                self.set(self.output_valve, 0)
                self.send(self.output_valve, 0, self.plc_addr)
                self.set(self.pump, 0)
                self.send(self.pump, 0, self.plc_addr)

            ## maybe do some stuff with flow meters
            # flow_rate = float(self.receive(self.flow_sensor, self.flow_plc_addr))
            # print(f"DEBUG {self.name} - Received flow rate: {flow_rate}")
            # self.send()



            time.sleep(PLC_PERIOD_SEC)
            count += 1


# if __name__ == "__main__":
    #     plc1 = SwatPLC1(
    #         name='plc1',
    #         state=STATE,
    #         protocol=PLC1_PROTOCOL,
    #         memory=PLC1_DATA,
    #         disk=PLC1_DATA)