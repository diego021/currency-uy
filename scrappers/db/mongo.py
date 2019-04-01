import datetime
from mongoengine import *

NAME = 'CurrencyUy' # DB Name
PORT = 27017        # Port
IP = 'localhost'    # Target
connect(NAME, host=IP, port=PORT)

#Collections
class Rates(EmbeddedDocument):
    rates = DictField(required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow())

class CurrencyExchange(Document):
    name = StringField(required=True)
    data = ListField(EmbeddedDocumentField(Rates))
    date_modified = DateTimeField(default=datetime.datetime.utcnow())

    meta = {
        'collection': 'currency_exchange',
        'indexes': [
            {'fields': ['name']}
        ],
        'ordering': ['-name']
    }

def upsert_exchange_rates(currency_exchange_name, rates):
    timestamp = datetime.datetime.utcnow()
    try:
        exchange = CurrencyExchange.objects.get(name=currency_exchange_name)
    except Exception:
        exchange = CurrencyExchange(name=currency_exchange_name)

    exchange.data.append(Rates(rates=rates, date_created=timestamp))
    exchange.update(date_modified=timestamp)
    exchange.save()

