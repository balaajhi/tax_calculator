import asyncio
import aiohttp
from flask import Flask, request, jsonify
from .tax_bracket import TaxBracket
from logger import logger

app = Flask(__name__)


class TaxCalculatorController:
    """Controller class for tax calculation operations."""

    def __init__(self):
        """Initialize TaxCalculatorController."""
        self.tax_brackets_cache = {}

    async def fetch_tax_brackets(self, year):
        """Fetch tax brackets for a given year from an external API and store them in the cache."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://0.0.0.0:5001/tax-calculator/tax-year/{year}') as response:
                    if response.status == 200:
                        tax_brackets_data = await response.json()
                        # print("tax_brackets_data: \n",tax_brackets_data)
                        # self.tax_brackets_cache[year] = [TaxBracket(**bracket_data) for bracket_data in tax_brackets_data.get('tax_brackets', [])]
                        brackets = []
                        for bracket_data in tax_brackets_data.get('tax_brackets', []):
                            min_income = bracket_data['min']
                            max_income = bracket_data.get('max')
                            rate = bracket_data['rate']
                            brackets.append(TaxBracket(min_income, max_income, rate))
                        self.tax_brackets_cache[year] = brackets
                    else:
                        # pass
                        logger.error(f"Failed to fetch tax brackets for year {year}. Status code: {response.status}")
        except Exception as e:
            # pass
            logger.error(f"Failed to fetch tax brackets for year {year}. Error: {e}")

    async def get_tax_brackets(self, year):
        """Retrieve tax brackets for a given year from the cache or fetch them if not already cached."""
        if year not in self.tax_brackets_cache:
            await self.fetch_tax_brackets(year)
        return self.tax_brackets_cache.get(year, [])

    async def calculate_taxes(self, salary, tax_year):
        """Calculate taxes owed based on the provided salary and tax year."""
        try:
            if tax_year not in [2019, 2020, 2021, 2022]:
                return jsonify({'error': 'Invalid tax year. Only years 2019, 2020, 2021, and 2022 are supported.'}), 400

            tax_brackets = await self.get_tax_brackets(tax_year)
            if not tax_brackets:
                return jsonify({'error': 'Failed to fetch tax brackets for the specified year.'}), 500

            total_tax = 0
            tax_breakdown = []

            for bracket in tax_brackets:
                if bracket.max_income is not None:
                    taxable_amount = min(salary, bracket.max_income) - bracket.min_income
                else:
                    taxable_amount = salary - bracket.min_income

                if taxable_amount <= 0:
                    continue

                tax_for_bracket = taxable_amount * bracket.rate
                total_tax += tax_for_bracket
                tax_breakdown.append({'min': bracket.min_income, 'max': bracket.max_income, 'tax': tax_for_bracket})

            effective_tax_rate = total_tax / salary * 100

            result = {
                'total_tax': round(total_tax, 2),
                'tax_breakdown': tax_breakdown,
                'effective_tax_rate': round(effective_tax_rate, 2)
            }

            return jsonify(result)
        except Exception as e:
            # logger.error(f"Error calculating taxes: {str(e)}")
            return jsonify({'error': 'An error occurred while calculating taxes.'}), 500


controller = TaxCalculatorController()


@app.route('/tax-calculator', methods=['GET'])
async def calculate_taxes():
    """Endpoint to calculate taxes owed based on the provided salary and tax year."""
    salary = request.args.get('salary', type=float)
    tax_year = request.args.get('tax_year', type=int)
    if salary is None or tax_year is None:
        return jsonify({'error': 'Salary and tax_year parameters are required.'}), 400
    return await controller.calculate_taxes(salary, tax_year)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(controller.fetch_tax_brackets(2019))
    app.run(debug=True)
