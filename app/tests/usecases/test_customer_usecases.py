import pytest
from unittest.mock import Mock
from entities.customer import Customer
from usecases.customers_usecases import Customer_usecases

@pytest.fixture
def mock_repository():
    return Mock()

def test_add_customer(mock_repository):
    usecases = Customer_usecases(mock_repository)
    customer_data = {
        'customerKey': 1,
        'educationLevel': 'Masters',
        'occupation': 'Engineer',
        'homeOwner': True,
        'prefix': 'Mr.',
        'firstName': 'John',
        'lastName': 'Doe',
        'birthDate': '12/12/1990',
        'maritalStatus': 'Single',
        'gender': 'Male',
        'emailAddress': 'john.doe@example.com',
        'annualIncome': 100000,
        'totalChildren': 0
    }
    customer = Customer(**customer_data)
    usecases.add_customer(customer)

    mock_repository.add_customer.assert_called_once_with(customer)

def test_get_customer(mock_repository):
    usecases = Customer_usecases(mock_repository)
    customer_data = {
        'customerKey': 1,
        'educationLevel': 'Masters',
        'occupation': 'Engineer',
        'homeOwner': True,
        'prefix': 'Mr.',
        'firstName': 'John',
        'lastName': 'Doe',
        'birthDate': '12/12/1990',
        'maritalStatus': 'Single',
        'gender': 'Male',
        'emailAddress': 'john.doe@example.com',
        'annualIncome': 100000,
        'totalChildren': 0
    }
    expected_customer = Customer(**customer_data)
    mock_repository.get_customer.return_value = expected_customer

    customer = usecases.get_customer(1)

    assert customer.customerKey == expected_customer.customerKey
    assert customer.educationLevel == expected_customer.educationLevel
    assert customer.occupation == expected_customer.occupation
    assert customer.homeOwner == expected_customer.homeOwner
    assert customer.prefix == expected_customer.prefix
    assert customer.firstName == expected_customer.firstName
    assert customer.lastName == expected_customer.lastName
    assert customer.birthDate == expected_customer.birthDate
    assert customer.maritalStatus == expected_customer.maritalStatus
    assert customer.gender == expected_customer.gender
    assert customer.emailAddress == expected_customer.emailAddress
    assert customer.annualIncome == expected_customer.annualIncome
    assert customer.totalChildren == expected_customer.totalChildren

if __name__ == "__main__":
    pytest.main()
