# -*- coding: utf-8 -*-
#
# Hiveeyes MicroPython Datalogger
# https://github.com/hiveeyes/hiveeyes-micropython-firmware
#
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
import settings
from terkin.datalogger import TerkinDatalogger


class DummySensor:

    def read(self):
        # Fake measurement.
        data = {"temperature": 42.84, "humidity": 83}
        return data


class ExampleDatalogger(TerkinDatalogger):
    """
    Yet another data logger. This is for MicroPython.
    """

    # Naming things.
    name = 'Example MicroPython Datalogger'

    def register_sensors(self):
        """
        Add your sensors here.
        """

        # First, spin up the built-in sensors.
        super().register_sensors()

        # Add some sensors.
        self.device.tlog('Registering custom sensors')

        # Add a new sensor. This is just an example sensor.
        sensor = DummySensor()
        self.register_sensor(sensor)


def main():
    """Start the data logger application."""
    datalogger = ExampleDatalogger(settings)
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
