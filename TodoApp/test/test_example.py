import pytest  # pyright: ignore[reportMissingImports]


# validate Integers
def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 2


# validate Instances
def test_is_instance():
    assert isinstance('this is string', str)        # Pass
    assert not isinstance('10',  int)               # Pass
    assert isinstance(10, int)                      # Pass
#    assert isinstance('this is a integer', int)      #Fail


# Validete boolean
def test_boolean():
    assert type('Hello' is str)         # Pass
    assert type(10 is int)              # Pass
    assert type(10 is str)              # Pass
    assert type("hello" is int)         # Pass   This checks the type of (True/False)
#    assert type(hello is str)           # Fail


# Validate Types
def test_type():
    arr = [1, 2, 5, 7]
    any_arr = [False, False]
    assert 1 in arr
    assert 8 not in arr
    assert all(arr)
    assert not any(any_arr)



# Validate Objects
class Student:
    def __init__(self, first_name: str, last_name: str, major: str, graduation_year:int):
        self.first_name=first_name
        self.last_name=last_name
        self.major=major
        self.graduation_year=graduation_year

@pytest.fixture   # must import pytest
def default_student():
    return Student("Suman", "Yadav", "Computer Science", 2027)
    return Student("Aman", "Bhagat", "Electrical", 2026)



def test_student_initialization(default_student):
    s = Student("Suman", "Yadav", "Computer Science", 2027)
    assert s.first_name=="Suman", "this is first name"
    assert s.last_name=="Yadav" , "this is last name"
    assert s.major=="Computer Science", "this is major"
    assert s.graduation_year==2027, "this is graduation year"