


# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.




try:
    import os
    import sys
    import datetime
    import time
    import boto3
    import Adafruit_DHT
    import threading
    print("All Modules Loaded ...... ")
except Exception as e:
    print("Error {}".format(e))


class MyDb(object):

    def __init__(self, Table_Name='DHT'):
        self.Table_Name=Table_Name

        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(Table_Name)

        self.client = boto3.client('dynamodb')

    @property
    def get(self):
        response = self.table.get_item(
            Key={
                'Sensor_Id':"1"
            }
        )

        return response

    def put(self, Sensor_Id='' , Temperature='', Humidity=''):
        self.table.put_item(
            Item={
                'Sensor_Id':Sensor_Id,
                'Temperature':Temperature,
                'Humidity' :Humidity
            }
        )

    def delete(self,Sensor_Id=''):
        self.table.delete_item(
            Key={
                'Sensor_Id': Sensor_Id
            }
        )

    def describe_table(self):
        response = self.client.describe_table(
            TableName='Sensor'
        )
        return response

    @staticmethod
    def sensor_value():

        pin = 23
        sensor = Adafruit_DHT.DHT11

        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return temperature, humidity


def main():
    global counter

    threading.Timer(interval=10, function=main).start()
    obj = MyDb()
    Temperature , Humidity = obj.sensor_value()
    obj.put(Sensor_Id=str(counter), Temperature=str(Temperature), Humidity=str(Humidity))
    counter = counter + 1
    print("Uploaded Sample on Cloud T:{},H{} ".format(Temperature, Humidity))


if __name__ == "__main__":
    global counter
    counter = 0
    main()









