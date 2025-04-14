class Dima:
    def __init__(self, name=None, surname=None, birth_year=None):
        self.name = name
        self.surname = surname
        self.birth_year = birth_year

    def get_course(self):
        return max(2025 - (self.birth_year + 16) + 1, 1) if self.birth_year else None

    def get_full_name_list(self):
        return [self.name, self.surname]


student = Dima("Діма", "Миколайчук", 2008)

print("Курс:", student.get_course())
print("ПІБ:", student.get_full_name_list())
