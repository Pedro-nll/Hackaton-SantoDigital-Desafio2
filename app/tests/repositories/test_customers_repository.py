import pytest
import sqlite3
from entities.customer import Customer
from repositories.sqlite.customers_repository import SQLiteCustomersRepository

@pytest.fixture
def db():
    # Utiliza um banco de dados SQLite em memória para os testes
    return ':memory:'

@pytest.fixture
def repository(db):
    return SQLiteCustomersRepository(db)

def test_add_and_get_customer(repository):
    customer = Customer(
        customerKey=1,
        educationLevel="Bachelor's",
        occupation="Engineer",
        homeOwner=True,
        prefix="Mr.",
        firstName="John",
        lastName="Doe",
        birthDate="1985-01-01",
        maritalStatus="Single",
        gender="Male",
        emailAddress="john.doe@example.com",
        annualIncome=75000.00,
        totalChildren=2
    )
    
    # Adiciona o cliente no repositório
    repository.add_customer(customer)
    
    # Recupera o cliente do repositório
    retrieved_customer = repository.get_customer(1)
    
    # Verifica se o cliente recuperado é igual ao cliente inserido
    assert retrieved_customer.customerKey == customer.customerKey
    assert retrieved_customer.educationLevel == customer.educationLevel
    assert retrieved_customer.occupation == customer.occupation
    assert retrieved_customer.homeOwner == customer.homeOwner
    assert retrieved_customer.prefix == customer.prefix
    assert retrieved_customer.firstName == customer.firstName
    assert retrieved_customer.lastName == customer.lastName
    assert retrieved_customer.birthDate == customer.birthDate
    assert retrieved_customer.maritalStatus == customer.maritalStatus
    assert retrieved_customer.gender == customer.gender
    assert retrieved_customer.emailAddress == customer.emailAddress
    assert retrieved_customer.annualIncome == customer.annualIncome
    assert retrieved_customer.totalChildren == customer.totalChildren