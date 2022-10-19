from rabbit.rabbit_concumer import RabbitConsumerObject
from kv_part_gen.DataInstance import DataInstance
import json


def main():

    rabbit = RabbitConsumerObject(queue_name='DataToGenerate', callback=callback)
    rabbit.consume()


def callback(ch, method, properties, body):
    data = json.loads(body)
    airlines = int(data['airlines'])
    customers = int(data['customers'])
    flights_per_airline = int(data['flights_per_airline'])
    tickets_per_customer = int(data['tickets_per_customer'])
    db_data = DataInstance(airlines=airlines, customers=customers, flights_per_airline=flights_per_airline,
                           tickets_per_customer=tickets_per_customer)
    db_data.generate_data()
    return

if __name__ == '__main__':
    main()