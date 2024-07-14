class Customer:
    def __init__(self, customerKey: int, educationLevel: str, occupation: str, homeOwner: bool, prefix: str, firstName: str, lastName: str, birthDate: str, maritalStatus: str, gender: str, emailAddress: str, annualIncome: float, totalChildren: int):
        self.customerKey = customerKey
        self.educationLevel = educationLevel
        self.occupation = occupation
        self.homeOwner = homeOwner
        self.prefix = prefix
        self.firstName = firstName
        self.lastName = lastName
        self.birthDate = birthDate
        self.maritalStatus = maritalStatus
        self.gender = gender
        self.emailAddress = emailAddress
        self.annualIncome = annualIncome
        self.totalChildren = totalChildren
        
    def __str__(self):
        return f"Customer: {self.firstName} {self.lastName}, Email: {self.emailAddress}, Education Level: {self.educationLevel}, Occupation: {self.occupation}, Home Owner: {self.homeOwner}, Customer Key: {self.customerKey}, Prefix: {self.prefix}, Birth Date: {self.birthDate}, Marital Status: {self.maritalStatus}, Gender: {self.gender}, Annual Income: {self.annualIncome}, Total Children: {self.totalChildren}"
