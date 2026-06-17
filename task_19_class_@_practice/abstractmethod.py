from abc import ABC, abstractmethod
class Employee(ABC):
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    @abstractmethod
    def calculate_pay(self):
        pass
class CommissionEmployee(Employee):
    def __init__(self, name, base_salary, sales_amount, commission_rate):
        self.commission_rate = commission_rate
        self.sales_amount = sales_amount
        super().__init__(name, base_salary)
    def calculate_pay(self):
        total_pay = self.base_salary + (self.sales_amount * self.commission_rate)
        return f"Pay for {self.name}: ${total_pay}"

def process_payroll(employee_obj):
    return employee_obj.calculate_pay()

emp = CommissionEmployee("Jane Doe", 3000.0, 10000.0, 0.05)
print(process_payroll(emp))
