# Docs

to set up key auth for kong admin api

```text
Usage: setup.py [OPTIONS]

Options:
  -k, --kong-server TEXT
  -t, --token TEXT
  -h, --token-header TEXT
  --help                   Show this message and exit.

```

## usage

```text
python3 setup.py -k 'http://localhost:8001' -t {your-token} -h {header-field-for-token}
```
