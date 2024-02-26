from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
import config


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename


    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        while True:
            try:
                accelerometerData = self.read_acceleromete_data()
                gpsData = self.read_gps_data()
                parkingData = self.read_parking_data()
                return AggregatedData(accelerometerData, gpsData, datetime.now(), parkingData, config.USER_ID)
            except StopIteration: self.start_reading()

    def read_acceleromete_data(self):
        column = next(reader(self.accelerometer_file))
        return Accelerometer(*map(float, column))

    def read_gps_data(self):
        column = next(reader(self.gps_file))
        return Gps(*map(float, column))

    def read_parking_data(self):
        empty_count, latitude, longitude = map(float, next(reader(self.parking_file)))
        gps = Gps(latitude, longitude)
        return Parking(empty_count, gps)

    def start_reading(self):
        """Метод повинен викликатись перед початком читання даних"""
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        self.parking_file = open(self.parking_filename, 'r')
        next(self.accelerometer_file)
        next(self.gps_file)
        next(self.parking_file)
