from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accelerometer_file = None
        self.gps_file = None

    def startReading(self):
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')

    def stopReading(self):
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()

    def read(self) -> AggregatedData:
        accelerometer_data = self._read_accelerometer_data()
        gps_data = self._read_gps_data()
        time = datetime.now()

        return AggregatedData(accelerometer=accelerometer_data, gps=gps_data, time=time)

    def _read_accelerometer_data(self) -> Accelerometer:
        if not self.accelerometer_file:
            raise ValueError("Accelerometer file not opened")

        line = self.accelerometer_file.readline()
        while line and (line.startswith('x') or line.startswith('X')):
            # Пропускаємо заголовок (якщо він є)
            line = self.accelerometer_file.readline()

        if not line:
            raise EOFError("End of file reached")

        try:
            x, y, z = map(int, line.strip().split(','))
        except ValueError:
            raise ValueError(f"Invalid data format in accelerometer file: {line}")

        return Accelerometer(x=x, y=y, z=z)


    def _read_gps_data(self) -> Gps:
        if not self.gps_file:
            raise ValueError("GPS file not opened")

        line = self.gps_file.readline()
        while line and (line.startswith('longitude') or line.startswith('Latitude')):
            # Пропускаємо заголовок (якщо він є)
            line = self.gps_file.readline()

        if not line:
            raise EOFError("End of file reached")

        try:
            longitude, latitude = map(float, line.strip().split(','))
        except ValueError:
            raise ValueError(f"Invalid data format in GPS file: {line}")

        return Gps(longitude=longitude, latitude=latitude)