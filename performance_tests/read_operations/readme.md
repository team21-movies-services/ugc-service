
## Запуск тестов

```
$ make test-up-postgres
$ make test-up-mongo
```

```
$ PYTHONPATH=./src/app poetry run python3 performance_tests/read_operations/tests/postgres_test.py
$ PYTHONPATH=./src/app poetry run python3 performance_tests/read_operations/tests/mongo_test.py  
```
