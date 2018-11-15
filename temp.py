# -*- coding: utf-8 -*-

import unittest
import logging

def add(numbers):
    logger = logging.getLogger('addLogger')
    sum = 0
    raise_exception = False
    exception_msg = "negatives not allowed"
    delimiters = [',']
    numbers_lines = numbers.split('\n')
    if(numbers[0:2]=="//" and len(numbers_lines[0]) >= 3):
        first_line = numbers_lines[0]
        if(len(first_line) == 3):
            delimiters = [first_line[2]]
        elif(first_line[2]=="["):
            i = 2
            bracket_open = True
            delimiters = []
            delimiter = ''
            while(i < len(first_line)-1):
                i+=1
                if(first_line[i]=="]" and (i+1 == len(first_line) or first_line[i+1]=="[") and bracket_open):
                    bracket_open = False
                    delimiters += [delimiter]
                    delimiter = ''
                elif(first_line[i]=="[" and (not bracket_open)):
                    bracket_open = True
                elif(bracket_open):
                    delimiter += first_line[i]
        numbers_lines = numbers_lines[1:]
        
    if(numbers!=''):
        string_delimited = numbers_lines
        for delim in delimiters:
            string_tmp = []
            for part in string_delimited:
                string_tmp += part.split(delim)
            string_delimited = string_tmp
        for i in string_delimited:
            if (int(i) < 0):
                raise_exception = True
                exception_msg += ", " + i
            elif (int(i) <= 1000):
                sum += int(i)
    if(raise_exception):
        raise Exception(exception_msg)
    logger.info('result: ' + str(sum))
    return sum

class TestMethods(unittest.TestCase):

    def test_add_empty(self):
        self.assertEqual(add(""), 0)
        
    def test_add_one_number(self):
        self.assertEqual(add("3"), 3)
        
    def test_add_two_numbers(self):
        self.assertEqual(add("3,4"), 7)
        
    def test_add_numbers_two_delimiters(self):
        self.assertEqual(add("1\n2,3"), 6)
        
    def test_add_numbers_chosen_delimiter(self):
        self.assertEqual(add("//;\n1\n2;3"), 6)
        
    def test_add_numbers_negative_number_exception(self):
        with self.assertRaises(Exception) as cm:
            add("1\n2,-8,3")
        self.assertEqual("negatives not allowed, -8", cm.exception.args[0])
        
    def test_add_numbers_several_negative_numbers_exception(self):
        with self.assertRaises(Exception) as cm:
            add("1\n2,-8,-3")
        self.assertEqual("negatives not allowed, -8, -3", cm.exception.args[0])
        
    def test_add_numbers_above_1000(self):
        self.assertEqual(add("1001\n2,3"), 5)
        
    def test_add_numbers_delimiter_any_length(self):
        self.assertEqual(add("//[***]\n1***2***3"), 6)
        
    def test_add_numbers_several_delimiters(self):
        self.assertEqual(add("//[*][%]\n1*2%3"), 6)
        
    def test_add_numbers_several_long_delimiters(self):
        self.assertEqual(add("//[*er][%*]]\n1*er2%*]3"), 4)
        
    def test_add_numbers_sum_result_logged(self):
        with self.assertLogs('addLogger', level='INFO') as cm:
            add("3\n2,3")
            add("1\n2,3")
            self.assertEqual(cm.output, ['INFO:addLogger:result: 8',
                                         'INFO:addLogger:result: 6'])

if __name__ == '__main__':
    unittest.main()