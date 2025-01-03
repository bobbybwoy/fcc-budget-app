class Category:
    # Constructor with the name and ledger instance variables defined
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        # If there is sufficient funds, complete the withdrawal
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else: return False

    def get_balance(self):
        # Set the computed balance to 0
        balance = 0

        # Sum up each ledger item's amount
        for item in self.ledger:
            balance += item['amount']

        return balance

    def transfer(self, amount, category):
        # Ensure that the category being passed is of type 'Category'
        if not isinstance(category, Category):
            return False

        # Ensure that the transfer is taking place with itself
        if self == category:
            return False

        # If there is sufficient funds, complete the transfer
        if self.check_funds(amount):
            self.withdraw(amount, 'Transfer to %s' % category.name)
            category.deposit(amount, 'Transfer from %s' % self.name)
            return True
        else: return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True

    def __repr__(self):
        FILLER_CHAR = '*'
        output = ''

        # Centre the heading with filler character
        output += self.name.center(30, FILLER_CHAR) + '\n'

        # for the ledger items for output
        for item in self.ledger:

            line = '{:23}{:7.2f}\n'.format(item['description'][:23], item['amount'])
            output += line

        output += 'Total: {:.2f}'.format(self.get_balance())
        return output

def create_spend_chart(categories):
    # Check if the parameter is a list
    if not isinstance(categories, list):
        return "Error: This is not a list"

    # Ensure that the number of categories is not more than four
    if len(categories) > 4:
        return "Error: There are too many categories"

    # Check if the supplied list contain only Category instances
    for category in categories:
        if not isinstance(category, Category):
            return f"Error: Not a category ({category})"

    # output = 'Percentage spent by category\n'
    output = 'Percentage spent by category'
    total_spend = 0
    category_spend = []
    max_name_len = 0
    
    # Calculate each category spend and the total spend
    for category in categories:
        if len(category.name) > max_name_len: max_name_len = len(category.name)

        amount = 0
        for item in category.ledger:
            if item['amount'] < 0:
                amount += -(item['amount'])

        category_spend.append({"category_name": category.name, "spend": amount})
        total_spend += round(amount, 2)

    # Create the bar charts
    for cs_obj in category_spend:
        bar_size = int(cs_obj['spend'] / total_spend * 10) + 1
        cs_obj['bar_size'] = bar_size


    # Output the bar charts
    for i in range(10, -1, -1):
        # Add the percentage labels
        output += f"\n{str(i * 10).rjust(3)}| "

        # Add the bar chart to the output
        for cs_obj in category_spend:
            if cs_obj['bar_size'] > i: output  += 'o'.ljust(3)
            else: output += ' '.ljust(3)

    # Output the bar under the bar charts
    no_of_dashes = len(category_spend) * 3 + 1
    output += f"\n{str.rjust('-'*no_of_dashes, (3 + no_of_dashes + 1))}"

    # Create the category name label beneath each bar chart
    for i in range(max_name_len):
        output += f"\n{' '.rjust(5)}"
        for cs_obj in category_spend:
            # Determine if the character should be a letter of the
            # of the category or a space
            if i < len(cs_obj['category_name']):
                output += cs_obj['category_name'][i].ljust(3)
            else: output += ' '.ljust(3)

    # Return the completed chart
    return output