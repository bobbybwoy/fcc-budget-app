import unittest

def main():
    # unittest.main(module='test_module', verbosity=2)
    unittest.main(module='test_module', verbosity=2, exit=False)
    unittest.main(module='test_module_fcc', verbosity=2)

############################## Main Program ############################
if __name__ == '__main__':
    main()