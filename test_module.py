import unittest
import budget

class TestCategory(unittest.TestCase):
    def setUp(self):
        self.food = budget.Category('Food')
        self.clothing = budget.Category('Clothing')
        self.entertainment = budget.Category('Entertainment')
        self.household_bills = budget.Category("Household Bills")
        self.mortgage = budget.Category("Mortgage")
        self.notCategoryInstance = 'Not a category'

    def tearDown(self):
        self.food = None
        self.clothing = None
        self.entertainmentter = None
        self.notCategoryInstance = None

    def test_make_a_deposit_with_no_amt_no_desc(self):
        self.food.deposit(0)
        self.assertEqual(
            self.food.ledger[0],
            {"amount": 0, "description": ""},
            "Expected to have a ledger item eith zero amount and no description"
        )
        self.assertEqual(
            self.food.get_balance(),
            0,
            "Expected that the balance is zero"
        )

    def test_make_a_deposit_with_amt_no_desc(self):
        self.food.deposit(100)
        self.assertEqual(
            self.food.ledger[0],
            {"amount": 100, "description": ""},
            "Expected to have a ledger item with an amount of 100 and no description"
        )
        self.assertEqual(
            self.food.get_balance(),
            100,
            "Expected that the balance will be 100"
        )

    def test_make_a_deposit_with_no_amt_with_desc(self):
        self.food.deposit(0, "no amount deposited")
        self.assertEqual(
            self.food.ledger[0],
            {"amount": 0, "description": "no amount deposited"}
        )
        self.assertEqual(
            self.food.get_balance(),
            0,
            "Expected that the balance is zero"
        )

    def test_check_funds_where_sufficient_funds_available(self):
        self.food.deposit(100, "initial deposit")
        self.assertEqual(
            self.food.check_funds(10),
            True,
            "Expected that checking the funds (100) for amount (10) will return true"
        )

    def test_check_funds_where_insufficient_funds_available(self):
        self.food.deposit(100, "initial deposit")
        self.assertEqual(
            self.food.check_funds(101),
            False,
            "Expected that checking the funds (100) for amount (101) will return false"
        )

    def test_check_funds_for_zero_amount_with_sufficient_funds(self):
        self.food.deposit(100, "initial deposit")
        self.assertEqual(
            self.food.check_funds(0),
            True,
            "Expected that checking the funds (100) with zero amount will return True"
        )

    def test_check_funds_for_zero_amount_with_zero_balance(self):
        self.food.deposit(0, "zero balance")
        self.assertEqual(
            self.food.check_funds(0),
            True,
            "Expected that checking the funds with zero balance for zero amount will return true"
        )

    def test_make_a_withdrawal_with_sufficient_funds(self):
        self.food.deposit(100, "initial deposit")
        self.assertEqual(
            self.food.withdraw(10, "cash"),
            True,
            "Expected that withdrawing 10 from the funds (100) will return true"
        )
        self.assertEqual(
            self.food.ledger[1],
            {"amount": -10, "description": "cash"},
            "Expected that the ledger will contain an entry for the cash withdrawal"
        )
        self.assertEqual(
            self.food.get_balance(),
            90,
            "Expected that the balance will be 90 (100 - 10)"
        )

    def test_make_a_withdrawal_with_insufficient_funds(self):
        self.food.deposit(5, "Initial deposit")
        self.assertEqual(
            self.food.withdraw(10, "cash"),
            False,
            "Expected that withdrawing 10 from the funds (5) will return false"
        )
        # TODO: Add an assert for the entry in the ledger
        self.assertEqual(
            len(self.food.ledger),
            1,
            "Expected that no entry created for the withdrawal"
        )

    def test_make_a_withdrawal_resulting_in_zero_balance(self):
        self.food.deposit(10, "zero balance")
        self.assertEqual(
            self.food.withdraw(10, "cash"),
            True,
            "Expected that withdrawing 10 from the funds (10) will return true"
        )
        # TODO: Add an assert for the entry in the ledger
        self.assertEqual(
            self.food.ledger[1],
            {"amount": -10, "description": "cash"},
            "Expected that the ledger will contain an entry for the cash withdrawal"
        )
        self.assertEqual(
            self.food.get_balance(),
            0,
            "Expected that the balance will be zero"
        )

    def test_get_a_balance(self):
        self.food.deposit(100, "initial deposit")
        self.assertEqual(
            self.food.get_balance(),
            100,
            "Expected that the balance return will be 100"
        )
        self.food.deposit(200, "additional funds made available")
        self.assertEqual(
            self.food.get_balance(),
            300,
            "Expected that the balance will have increased to 300"
        )
        self.food.withdraw(20, "delicious KFC all round!")
        self.assertEqual(
            self.food.get_balance(),
            280,
            "Expected that the balance will have decreased to 280"
        )

    def test_transfer_funds_to_category_with_sufficient_funds(self):
        # Add funds to the Food and Clothing categories
        self.food.deposit(200, "initial deposit")
        self.clothing.deposit(200, "initial deposit")

        self.assertEqual(
            self.food.transfer(100, self.clothing),
            True,
            "Expected that the transfer from Food to Clothing will return true"
        )
        self.assertEqual(
            self.food.ledger[1],
            {"amount": -100, "description": "Transfer to Clothing"},
            "Expected that the last entry in the ledger will contain the transfer entry"
        )
        self.assertEqual(
            self.clothing.ledger[1],
            {"amount": 100, "description": "Transfer from Food"}
        )
        self.assertEqual(
            self.food.get_balance(),
            100,
            "Expected that the balance for Food will be decreased by 100 to 100"
        )
        self.assertEqual(
            self.clothing.get_balance(),
            300,
            "Expected that the balance for Clothing will be increased by 100 to 300"
        )

    def test_transfer_funds_to_category_with_insufficient_funds(self):
        self.food.deposit(100, "initial deposit")

        self.assertEqual(
            self.food.transfer(101, self.clothing),
            False,
            "Expect that the transfor from Food to Clothing will return false"
        )
        self.assertEqual(
            len(self.food.ledger),
            1,
            "Expected that there will be no entry for the transfer to the Clothing Category"
        )
        self.assertEqual(
            len(self.clothing.ledger),
            0,
            "Expected that there will be no entry for the transfer from the Food Category"
        )
        self.assertEqual(
            self.food.get_balance(),
            100,
            "Expected that the balance for the Fodd Category will remain as 100"
        )

    def test_transfer_funds_to_nonexistent_category(self):
        self.food.deposit(100, "initial deposit")

        self.assertEqual(
            self.food.transfer(10, self.notCategoryInstance),
            False,
            "Expected that the transfor from Food to notCategoryInstance will return false"
        )
        self.assertEqual(
            len(self.food.ledger),
            1,
            "Expected that there will be no entry for the transfer from Food to notCategoryInstance"
        )
        self.assertEqual(
            self.food.get_balance(),
            100,
            "Expected that balance for the Food Category will remain as 100"
        )

    def test_display_category_with_no_entries(self):
        self.assertEqual(
            str(self.food),
            """*************Food*************
Total: 0.00""",
            "Expected that when the budget object is printed it will be just the header and total"
        )
        self.assertEqual(
            len(str(self.food).split('\n')[0]),
            30,
            "Expected that the length of the header will be 30 characters"
        )

    def test_display_category_with_one_entry(self):
        self.food.deposit(100, "initial deposit")
        self.assertEqual(
            str(self.food),
            """*************Food*************
initial deposit         100.00
Total: 100.00""",
            "Expected that the output will include the header and the only entry in the ledger"
        )

    def test_display_category_with_two_entries(self):
        self.food.deposit(100, "initial deposit")
        self.food.withdraw(10, "KFC for all")

        self.assertEqual(
            str(self.food),
            """*************Food*************
initial deposit         100.00
KFC for all             -10.00
Total: 90.00""",
            "Expected that the output will include the header and the only entry in the ledger"
        )

    def test_display_category_with_one_long_desc_entry(self):
        self.food.deposit(100, "initial deposit")
        self.food.withdraw(10, "Kentucky Fried Chicken for all")

        self.assertEqual(
            str(self.food),
            """*************Food*************
initial deposit         100.00
Kentucky Fried Chicken  -10.00
Total: 90.00""",
            "Expected that the output will include the header and the only entry in the ledger"
        )

    def test_create_spend_chart_with_one_category(self):
        self.food.deposit(100, "initial deposit")
        self.food.withdraw(10, "McD's")

        self.assertEqual(
            budget.create_spend_chart([self.food]),
            """Percentage spent by category
100| o  
 90| o  
 80| o  
 70| o  
 60| o  
 50| o  
 40| o  
 30| o  
 20| o  
 10| o  
  0| o  
    ----
     F  
     o  
     o  
     d  """,
            "Expected that the chart will represent bar of 100% for food"
        )

    def test_create_spend_chart_with_two_categories(self):
        # Transactions for Food Category
        self.food.deposit(200, "initial deposit")
        self.food.withdraw(10, "McD's")
        self.food.withdraw(50, "Restaurant bill")
        self.food.withdraw(20, "Groceries")
        # Transactions for Clothing Category
        self.clothing.deposit(500, "initial deposit")
        self.clothing.withdraw(200, "A suit")
        self.clothing.withdraw(50, "Shoes")

        self.assertEqual(
            budget.create_spend_chart([self.food, self.clothing]),
            """Percentage spent by category
100|       
 90|       
 80|       
 70|    o  
 60|    o  
 50|    o  
 40|    o  
 30|    o  
 20| o  o  
 10| o  o  
  0| o  o  
    -------
     F  C  
     o  l  
     o  o  
     d  t  
        h  
        i  
        n  
        g  """,
            "Expected that the chart will represent bars for Food (20) and Clothing (70)"
        )

    def test_create_spend_chart_with_four_categories(self):
        # Transactions for Food
        self.food.deposit(200, "initial deposit")
        self.food.withdraw(100, "Groceries")
        # Transactions for Clothing
        self.clothing.deposit(200, "initial deposit")
        self.clothing.withdraw(100, "Trousers and shoes")
        # Transactions for Entertainment
        self.entertainment.deposit(50, "initial deposit")
        self.entertainment.withdraw(10, "Cinema")
        # Transactions for Household Bills
        self.household_bills.deposit(500, "initial deposit")
        self.household_bills.withdraw(150, "Energy bills")

        self.assertEqual(
            budget.create_spend_chart(
                [self.food,
                self.clothing,
                self.entertainment,
                self.household_bills]
            ),
            """Percentage spent by category
100|             
 90|             
 80|             
 70|             
 60|             
 50|             
 40|          o  
 30|          o  
 20| o  o     o  
 10| o  o     o  
  0| o  o  o  o  
    -------------
     F  C  E  H  
     o  l  n  o  
     o  o  t  u  
     d  t  e  s  
        h  r  e  
        i  t  h  
        n  a  o  
        g  i  l  
           n  d  
           m     
           e  B  
           n  i  
           t  l  
              l  
              s  """,
            "Expected that the chart will represent bars for Food (20), Clothing (20), Entertainment (0), and Household Bills (40)"
        )

    def test_create_spend_chart_with_five_categories(self):
        # Transactions for Food
        self.food.deposit(200, "initial deposit")
        self.food.withdraw(100, "Groceries")
        # Transactions for Clothing
        self.clothing.deposit(200, "initial deposit")
        self.clothing.withdraw(100, "Trousers and shoes")
        # Transactions for Entertainment
        self.entertainment.deposit(50, "initial deposit")
        self.entertainment.withdraw(10, "Cinema")
        # Transactions for Household Bills
        self.household_bills.deposit(500, "initial deposit")
        self.household_bills.withdraw(150, "Energy bills")
        # Transactions for Mortgage
        self.mortgage.deposit(1500, "initial deposit")
        self.mortgage.withdraw(650, "Monthly payment with interest")

        self.assertEqual(
            budget.create_spend_chart(
                [self.food,
                self.clothing,
                self.entertainment,
                self.household_bills,
                self.mortgage]
            ),
            "Error: There are too many categories",
            "Expected that an error message will be returned"
        )

    def test_create_spend_chart_with_one_invalid_category(self):
        self.food.deposit(100, "initial deposit")
        self.food.withdraw(10, "Groceries")

        self.assertEqual(
            budget.create_spend_chart([self.food, self.notCategoryInstance]),
            "Error: Not a category (Not a category)",
            "Expected that an error will be produced stating that one category is invalid"
        )

    def test_create_spend_chart_with_a_category_but_not_in_list(self):
        self.food.deposit(100, "initial deposit")
        self.food.withdraw(10, "Groceries")

        self.assertEqual(
            budget.create_spend_chart(self.food),
            "Error: This is not a list",
            "Expected that an error will be produced stating that the imput is not a list"
        )

############################## Main Program ############################
if __name__ == '__main__':
    unittest.main()