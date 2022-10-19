import kivy
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, StringProperty
import json

from kv_part_gen.DataInstance import DataInstance
from errors import DataIsNotValid
from rabbit.rabbit_producer import RabbitProducerObject
from rabbit.rabbit_concumer import RabbitConsumerObject
from db.db_config import local_session
from db.db_repo import DbRepo
from threading import Thread


class InstanceGenerator(Widget):
    airline_companies = ObjectProperty(None)
    customers = ObjectProperty(None)
    flights_per_company = ObjectProperty(None)
    tickets_per_customer = ObjectProperty(None)
    my_progress_bar = ObjectProperty(None)
    alerts_label = StringProperty('')
    rabbit_producer = RabbitProducerObject('DataToGenerate')
    already_generated = False

    def update_progress_bar(self, value):
        self.ids.my_progress_bar.value = value

    def btn(self):
        if self.already_generated:
            self.ids.alerts_label.text = 'The data was already generated, please close the app.'
            return
        try:
            airlines = self.airline_companies.text
            customers = self.customers.text
            flights_per_company = self.flights_per_company.text
            tickets_per_customer = self.tickets_per_customer.text
            db_data_object = DataInstance(customers=customers, airlines=airlines,
                                          flights_per_airline=flights_per_company,
                                          tickets_per_customer=tickets_per_customer)
            db_data_object.validate_data()
            self.rabbit_producer.publish(json.dumps(db_data_object.__dict__()))
            self.already_generated = True
            self.ids.alerts_label.text = 'Generating Data...'

        except DataIsNotValid:
            self.ids.alerts_label.text = 'Data is not Valid!'


Builder.load_file('my6.kv')

dbgen = InstanceGenerator()


def get_db_gen():
    return dbgen


class MyApp(App):
    def build(self):
        return get_db_gen()


def callback(ch, method, properties, body):
    data = json.loads(body)
    progress_bar_value = list(data.values())[0]
    kivy_app = get_db_gen()
    kivy_app.ids.alerts_label.text = f'Generating {list(data.keys())[0]}'
    kivy_app.update_progress_bar(progress_bar_value)
    if progress_bar_value == 100:
        kivy_app.ids.alerts_label.text = 'The data was successfully generated!'


if __name__ == "__main__":

    repo = DbRepo(local_session)
    repo_thread = Thread(target=repo.reset_auto_inc_all)
    repo_thread.start()
    rabbit_consumer = RabbitConsumerObject(queue_name='GeneratedData', callback=callback)
    t1 = Thread(target=rabbit_consumer.consume)
    t1.setDaemon(True)
    t1.start()
    MyApp().run()