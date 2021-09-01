from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.


class Schema(models.Model):

    COMMA = ','
    SEMICOLON = ':'
    PIPE = '|'

    COLUMN_SEPARATORS = (
        (COMMA, 'Comma(,)'),
        (SEMICOLON, 'Semicolon(:)'),
        (PIPE, 'Pipe(|)'),
    )

    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'

    STRING_CHARACTERS = (
        (SINGLE_QUOTE, "Single-quote(')"),
        (DOUBLE_QUOTE, 'Double-quote (")'),
    )

    title = models.CharField(max_length=50)
    column_separator = models.CharField(
        max_length=1, choices=COLUMN_SEPARATORS, default=COMMA)
    string_character = models.CharField(
        max_length=1, choices=STRING_CHARACTERS, default=SINGLE_QUOTE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Column(models.Model):

    FULL_NAME = 'Full name'
    JOB = 'Job'
    EMAIL = 'Email'
    COMPANY = 'Company'
    INTEGER = 'Integer'

    COLUMN_TYPES = (
        (FULL_NAME, 'Full name'),
        (JOB, 'Job'),
        (EMAIL, 'Email'),
        (COMPANY, 'Company'),
        (INTEGER, 'Integer'),
    )

    name = models.CharField(max_length=50)
    column_type = models.CharField(
        max_length=10, choices=COLUMN_TYPES, default=INTEGER)
    start_value = models.IntegerField(blank=True, null=True)
    end_value = models.IntegerField(blank=True, null=True)
    order = models.PositiveIntegerField()
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DataSet(models.Model):

    READY = 'Ready'
    PROCESSING = 'Processing'

    Status = (
        (READY, 'Ready'),
        (PROCESSING, 'Processing')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=11, choices=Status, default=PROCESSING)
    created = models.DateField(auto_now_add=True)
    file = models.FileField()

    def __str__(self):
        return f'{self.schema.title}'

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)


    class Meta:
        ordering = ('-id',)
