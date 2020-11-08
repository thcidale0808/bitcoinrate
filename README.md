# Bitcoin Rate Solution

This is the repository of the Bitcoin Rate solution. It contains the following applications:
* API: Responsible to expose two endpoints: 
    * Get the BTC-USD latest rate from a local database.
    * Get the BTC-USD historical rates from a local database.
* Extractor: Responsible to constantly get the BTC-USD exchange rate from [Coinlayer](https://coinlayer.com) and save to a database.  

## Development Setup
This section contains the information required to configure and test the local environment

### Pre-requisites:
* [Pipenv](https://pypi.org/project/pipenv/) preferably using Brew (https://brew.sh/)
* Make
* Coinlayer API KEY

### Install Dependencies
```bash
make setup
```

### Run the unit tests:
```bash
make test
```

## Running locally
This section contains the information to setup and run each component locally

### Run Extractor
This will run the Extractor start save rates from Coinlayer Public API
```bash
make run-extractor
```

### Run API
This will create a local DB and run the API
```bash
make run-api
```
API will now be available on `http://localhost:5000`.
<br>

### API Contract Swagger
API documentation is in OpenAPI 3.0 format.
To view the docs:
```bash
make docs-view
```
Docs will now be served on `http://localhost:8080`


## Future Improvements
* Add security headers
* Add authentication
* Add CI configuration
* Create service and repository layers to abstract database and any other potential low level logic
* Use async web frameworks like FastAPI to run and wrap the API
* Add pagination for the historical bitcoin endpoint
* Add pre-hook commit to validate code format with black.
* Increase unit test coverage
* Add functional tests 
 
 