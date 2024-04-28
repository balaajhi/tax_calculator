# Tax Calculator

The Tax Calculator is a web application that calculates taxes owed based on the provided salary and tax year. It retrieves tax brackets for a given year from an external API and stores them in a cache for efficient computation.

## Features

- Calculate taxes owed based on salary and tax year.
- Fetch tax brackets from an external API.
- Log errors and information to a file app.log.

## Prerequisites

- Python 3.x
- Pipenv (for managing dependencies)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/balaajhi/tax_calculator.git
    cd tax_calculator
    ```

2. Install dependencies using Pipenv:

    ```bash
    pipenv install
    ```

3. Activate the virtual environment:

    ```bash
    pipenv shell
    ```
   
4. Running the Tests

    ```bash
    pytest
   
## Usage

### Running the Application

1. To run the application, use the following command:

    ```bash
    python tax_calculator.py

2. Test the application by running the following command:

    ```bash
    curl -X GET "http://localhost:8080/tax-calculator?salary=50000&tax_year=2022"
    ```
    http://localhost:8080/tax-calculator?salary=50&tax_year=2022
