import logging, time, os, requests
from sharedmodels.db import get_session_scope
from sharedmodels.models import Rate
from datetime import datetime
BATCH_INTERVAL = 60
TARGET_CURRENCY = 'USD'
SOURCE_CURRENCY = 'BTC'

logging.basicConfig(level=logging.INFO)


class RateExtractor:

    def __init__(self, session, bitcoin_url, access_key):
        self.session = session
        self.bitcoin_url = bitcoin_url
        self.access_key = access_key

    def get_bitcoin_rate(self):
        rates = []
        url = f'{self.bitcoin_url}?access_key={self.access_key}&target={TARGET_CURRENCY}'
        resp = requests.get(url)

        if resp.status_code == 200:
            rates.append({
                'value': resp.json()['rates'][SOURCE_CURRENCY],
                'currency_datetime':  datetime.utcfromtimestamp(resp.json()['timestamp'])
            })
        return rates

    def save_rate(self, rates):
        for rate in rates:
            Rate.create(session=self.session, source_currency=SOURCE_CURRENCY, target_currency=TARGET_CURRENCY, **rate)
        self.session.commit()

    def run(self):
        while 1:
            try:
                logging.info('Retrieving bitcoin rates')
                rate = self.get_bitcoin_rate()
                logging.info(f'Found {len(rate)} rate(s)')
                self.save_rate(rate)
                logging.info(f'Rate(s) saved successfully')
                time.sleep(BATCH_INTERVAL)
            except Exception as e:
                logging.error(e)
                time.sleep(BATCH_INTERVAL)


def main():
    bitcoin_api_url = os.environ.get('BITCOIN_URL')
    bitcoin_api_key = os.environ.get('BITCOIN_API_KEY')
    with get_session_scope() as session:
        rate_extractor = RateExtractor(session=session, bitcoin_url=bitcoin_api_url, access_key=bitcoin_api_key)
        rate_extractor.run()


if __name__ == '__main__':
    main()
