from utils.random import get_random_number

def test_get_random_number_range():
    """Test that random number is within expected range"""
    for _ in range(100):  # Test multiple times
        number = get_random_number()
        assert 0 <= number <= 10

def test_get_random_number_returns_integer():
    """Test that the function returns an integer"""
    number = get_random_number()
    assert isinstance(number, int)

def test_get_random_number_distribution():
    """Test that function returns different values"""
    numbers = [get_random_number() for _ in range(50)]
    assert len(set(numbers)) > 1  # At least 2 different numbers