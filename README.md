# firmament
Simple CLI utility to check HTTPS availability of sites

## Usage

`firmament` takes two arguments: an input file and an output file. The input file should be a plain text list of domains. The output file will be in CSV format.

```shell
$ python firmament.py input.txt output.csv
scan_all() is starting!
scan_site() called with example.com
OK: http://example.com (200)
OK: https://example.com (200)
Wrote a row of CSV output
scan_site() called with https://example.org
OK: http://example.org (200)
OK: https://example.org (200)
Wrote a row of CSV output
scan_all() is done!
```
