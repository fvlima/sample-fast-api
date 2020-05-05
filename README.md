[![Build Status](https://travis-ci.org/fvlima/sample-fast-api.svg?branch=master)](https://travis-ci.org/fvlima/sample-fast-api)
[![codecov](https://codecov.io/gh/fvlima/sample-fast-api/branch/master/graph/badge.svg)](https://codecov.io/gh/fvlima/sample-fast-api)

# sample-fast-api

A project to test a full async http request lifecycle with fastapi + gino + asyncpg

## next steps
- improve insert and update operations with db
- configurations to deal with postgres pool
- others...


## how to run locally
```
git clone https://github.com/fvlima/sample-fast-api.git
pip install poetry
poetry install -v
uvicorn sample_fast_api.main:app --reload
```

## some benchmarks
all tests were ran in a database with 1M users registereds

- 1000 requests with concurrency 10 retrieving 100 results per page
```
ab -n 1000 -c 10 -H "Authorization: Token a2a18886-d3a2-4774-8e5f-69f7e1057a7d" "http://127.0.0.1:8000/users/?q=User%20Name&limit=100&offset=0"

Complete requests: 1000
Failed requests: 0
Time per request: 64.130 [ms]
```

- 1000 requests with concurrency 10 retrieving 10 results per page
```
ab -n 1000 -c 10 -H "Authorization: Token a2a18886-d3a2-4774-8e5f-69f7e1057a7d" "http://127.0.0.1:8000/users/?q=User%20Name&limit=10&offset=0"

Complete requests: 1000
Failed requests: 0
Time per request: 14.512 [ms]
```

- 1000 requests with concurrency 10 fetching  user
```
ab -n 1000 -c 10 -H "Authorization: Token a2a18886-d3a2-4774-8e5f-69f7e1057a7d" "http://127.0.0.1:8000/users/24ca2936-5044-4d3e-bafe-904a68b0194f


Complete requests: 1000
Failed requests: 0
Time per request: 6.266 [ms]
```


- 1000 request with concurrency 10 posting users data
```
ab -n 1000 -c 10 -p user.json -m POST -H "Authorization: Token a2a18886-d3a2-4774-8e5f-69f7e1057a7d" http://127.0.0.1:8000/users/

Complete requests: 1000
Failed requests: 0
Time per request: 129.519 [ms]
```
