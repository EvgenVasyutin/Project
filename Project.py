class Expense:
    def __init__(self, amount, date, category, description):
        self.amount = amount
        self.date = date
        self.category = category
        self.description = description

    def validate_amount(self):
        try:
            amount = float(self.amount)
            if amount <= 0:
                return False
            return True
        except ValueError:
            return False

    def validate_date(self):
        return bool(self.date)

    def validate_category(self, available_categories):
        return self.category in available_categories

    def to_dict(self):
        return {
            'сума': self.amount,
            'дата': self.date,
            'категорія': self.category,
            'опис': self.description
        }


class Budget:
    def __init__(self, start_date, end_date, planned_amount):
        self.start_date = start_date
        self.end_date = end_date
        self.planned_amount = planned_amount
        self.expenses = []

    def plan_budget(self):
        total_expenses = self.get_total_expenses()
        return total_expenses <= self.planned_amount

    def add_expense(self, expense):
        self.expenses.append(expense)

    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses)


class Category:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def update_description(self, new_description):
        self.description = new_description


class Report:
    def __init__(self, expenses):
        self.expenses = expenses

    def generate_report(self):
        categories = {}
        for expense in self.expenses:
            if expense.category in categories:
                categories[expense.category] += expense.amount
            else:
                categories[expense.category] = expense.amount
        return categories

    def generate_text_report(self):
        report_text = "Звіт про витрати:\n"
        categories = self.generate_report()
        for category, amount in categories.items():
            report_text += f"{category}: ${amount}\n"
        return report_text


class ExpenseManager:
    def __init__(self):
        self.expenses = []
        self.budget = None
        self.categories = []

    def add_expense(self, amount, date, category, description):
        if not self.validate_expense_data(amount, date, category):
            print("Недійсні дані про витрати.")
            return None
        new_expense = Expense(amount, date, category, description)
        self.expenses.append(new_expense)
        return new_expense

    def validate_expense_data(self, amount, date, category):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False
        if not date:
            return False
        if category not in [cat.name for cat in self.categories]:
            return False
        return True

    def validate_budget_data(self, start_date, end_date, planned_amount):
        if not start_date or not end_date:
            return False
        if not isinstance(planned_amount, (int, float)) or planned_amount <= 0:
            return False
        return True

    def add_category(self, name, description):
        new_category = Category(name, description)
        self.categories.append(new_category)
        return new_category

    def create_budget(self, start_date, end_date, planned_amount):
        if not self.validate_budget_data(start_date, end_date, planned_amount):
            print("Недійсні дані бюджету.")
            return None
        self.budget = Budget(start_date, end_date, planned_amount)
        return self.budget

    def add_expense_to_budget(self, expense):
        if self.budget:
            self.budget.add_expense(expense)
        else:
            print("Бюджет ще не створено.")

    def generate_report(self):
        if self.expenses:
            report = Report(self.expenses)
            return report.generate_text_report()
        else:
            return "Витрати ще не зафіксовані."

    def get_expenses_by_category(self, category):
        return [expense for expense in self.expenses if expense.category == category]

    def update_category_description(self, category_name, new_description):
        for category in self.categories:
            if category.name == category_name:
                category.description = new_description
                return True
        return False

    def add_new_category(self, name, description):
        for category in self.categories:
            if category.name == name:
                print("Категорія вже існує")
                return False
        new_category = Category(name, description)
        self.categories.append(new_category)
        return True


expense_manager = ExpenseManager()

expense_manager.add_category("Одяг", "Витрати, пов'язані з покупкою одягу")
expense_manager.add_category("Подорожі", "Витрати, пов'язані з подорожами")

# Створимо бюджет
budget = expense_manager.create_budget("2024-04-01", "2024-04-30", 1000)
if budget:
    print("Бюджет створено успішно.")
else:
    print("Не вдалося створити бюджет.")

# Додамо витрати
expense_manager.add_expense(200, "2024-04-05", "Одяг", "Штани")
expense_manager.add_expense(150, "2024-04-10", "Їжа", "Обід")
expense_manager.add_expense(50, "2024-04-15", "Транспорт", "Таксі")

# Перевіримо стан бюджету
if budget.plan_budget():
    print("Бюджет сплановано успішно.")
else:
    print("Бюджет не вистачає на всі плановані витрати.")

# Додамо витрату до бюджету
expense_manager.add_expense_to_budget(Expense(300, "2024-04-20", "Подорожі", "Квитки на поїзд"))

# Згенеруємо звіт
print(expense_manager.generate_report())

# Додамо нову категорію
expense_manager.add_new_category("Розваги", "Витрати на розваги та відпочинок")

# Оновимо опис існуючої категорії
expense_manager.update_category_description("Їжа", "Витрати на їжу та напої")

# Згенеруємо звіт з оновленими даними
print(expense_manager.generate_report())
