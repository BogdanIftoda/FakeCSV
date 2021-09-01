from faker import Faker

fake = Faker()


def generate_fields_data(column_type, start_value, end_value):

    if column_type == 'Full name':
        return fake.name()
    if column_type == 'Job':
        return fake.job()
    if column_type == 'Email':
        return fake.email()
    if column_type == 'Company':
        return fake.company()
    if column_type == 'Integer':
        if start_value and end_value:
            return fake.pyint(start_value, end_value)
        if start_value:
            return fake.pyint(start_value, 99999)
        if end_value:
            return fake.pyint(0, end_value)
        return fake.random_int()
