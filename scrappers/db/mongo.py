from mongoengine import connect
from mongoengine import *
import datetime

# DB Name
NAME = 'CurrencyUy'

# DB Port
PORT = 27017

## DB Targets
local = 'localhost'
# __production = ''

connect(NAME, host=local, port=PORT)

#Collections
class Rates(EmbeddedDocument):
    currency = StringField(required=True)
    buy = FloatField(min_value=0.0, max_value=None)
    sell = FloatField(min_value=0.0, max_value=None)
    date_created = DateTimeField(default=datetime.datetime.utcnow)

class CurrencyExchange(Document):
    name = StringField(required=True)
    rates = ListField(EmbeddedDocumentField(Rates))
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'currency_exchange',
        'indexes': [
            {'fields': ['name']}
        ],
        'ordering': ['-name']
    }

def upsert_exchange_rates(currency_exchange_name, currency='', buy=0.0, sell=0.0):
    try:
        exchange = CurrencyExchange.objects.get(name=currency_exchange_name)
    except:
        exchange = CurrencyExchange(name=currency_exchange_name)

    exchange.rates.append(Rates(currency=currency, buy=buy, sell=sell))
    exchange.save()