import click
import logging
from chalk import log
import requests
import re
import csv

# Set up colorful logging
logger = logging.getLogger(__name__)
handler = log.ChalkHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

scheme_stripper_re = re.compile("""^http[s]?\:\/\/(.+)$""")


def strip_scheme(url):
    m = scheme_stripper_re.search(url)
    if m is not None:
        return m.group(1)
    else:
        return url


def as_http(url):
    return "http://%s" % (strip_scheme(url))


def as_https(url):
    return "https://%s" % (strip_scheme(url))


def scan_site(url, output):
    logger.debug("scan_site() called with %s" % (url))
    http_url = as_http(url)
    https_url = as_https(url)
    # logger.debug("http:  %s" % http_url)
    # logger.debug("https: %s" % https_url)

    stuff = {
        'url': url,
        'http': {
            'url': http_url,
            'result': None
        },
        'https': {
            'url': https_url,
            'result': None
        }
    }
    for scheme in ['http', 'https']:
        try:
            r = requests.get(stuff[scheme]['url'])
            if r.status_code == 200:
                logger.info(
                    "OK: %s (%d)" % (stuff[scheme]['url'], r.status_code)
                )
                stuff[scheme]['result'] = True
            else:
                raise Exception("Unexpected response code (it's not 200!!!)")

        except requests.exceptions.SSLError:
            # https://gist.github.com/anseljh/6c047495be34915a63d3
            logger.error("SSL error! %s" % stuff[scheme]['url'])
            stuff[scheme]['result'] = False

        except requests.exceptions.ConnectionError:
            logger.error("Couldn't connect to %s" % stuff[scheme]['url'])
            stuff[scheme]['result'] = False

    output.writerow([
        strip_scheme(url),
        stuff['http']['result'],
        stuff['https']['result']
    ])
    logger.debug("Wrote a row of CSV output")


@click.command()
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def scan_all(input, output):
    logger.debug("scan_all() is starting!")
    writer = csv.writer(output)
    for line in input:
        result = scan_site(line.strip(), writer)
    logger.debug("scan_all() is done!")
    output.close()

# def main():
if __name__ == '__main__':
    scan_all()
