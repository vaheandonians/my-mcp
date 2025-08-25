import pytest
from my_mcp.server import get_fibonacci_sequence


class TestGetFibonacciSequence:
    
    def test_negative_input(self):
        result = get_fibonacci_sequence(-1)
        assert result == "[]"
        
        result = get_fibonacci_sequence(-10)
        assert result == "[]"
    
    def test_zero_input(self):
        result = get_fibonacci_sequence(0)
        assert result == "[]"
    
    def test_one_element(self):
        result = get_fibonacci_sequence(1)
        assert result == "[0]"
    
    def test_two_elements(self):
        result = get_fibonacci_sequence(2)
        assert result == "[0, 1]"
    
    def test_small_sequences(self):
        result = get_fibonacci_sequence(3)
        assert result == "[0, 1, 1]"
        
        result = get_fibonacci_sequence(4)
        assert result == "[0, 1, 1, 2]"
        
        result = get_fibonacci_sequence(5)
        assert result == "[0, 1, 1, 2, 3]"
    
    def test_medium_sequence(self):
        result = get_fibonacci_sequence(10)
        assert result == "[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]"
    
    def test_larger_sequence(self):
        result = get_fibonacci_sequence(15)
        assert result == "[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]"
    
    def test_return_type_is_string(self):
        result = get_fibonacci_sequence(5)
        assert isinstance(result, str)
    
    def test_sequence_correctness(self):
        result = get_fibonacci_sequence(8)
        sequence = eval(result)
        
        assert len(sequence) == 8
        assert sequence[0] == 0
        assert sequence[1] == 1
        
        for i in range(2, 8):
            assert sequence[i] == sequence[i-1] + sequence[i-2]
