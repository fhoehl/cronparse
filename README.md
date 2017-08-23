# Cron parser

Run with Python 3 and the listed dependencies in `requirements.txt`.

```bash
cd cronparse
./cronparse.py */15 0 1,15 * 1-5 /usr/bin/find
```

## Tests

Tests are in `test_cronparse.py` and can be run with pytest.

```bash
cd cronparse
pytest
```

😊
