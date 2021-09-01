import csv
import os
from core.celery import app
from django.core.files import File
from faker import Faker

from .generate_data import generate_fields_data
from .models import Column, DataSet, Schema

fake = Faker()


@app.task
def create_csv(dataset_id, schema_id, rows):
    dataset = DataSet.objects.get(pk=dataset_id)
    schema = Schema.objects.get(pk=schema_id)
    columns = Column.objects.filter(schema=schema)
    column_separator = schema.column_separator
    string_character = schema.string_character
    file_name = f'{fake.random_int()}-{schema.title}.csv'

    columns_list = [column.name for column in columns]

    with open(f'media/{file_name}', 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC,
                            delimiter=column_separator, quotechar=string_character)
        writer.writerow(columns_list)
        for _ in range(rows):
            fake_data = [generate_fields_data(
                column.column_type, column.start_value, column.end_value) for column in columns]
            writer.writerow(fake_data)

        
        
    dataset.file.name = file_name
    dataset.status = DataSet.READY
    dataset.save()
    return