from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import ColumnForm, SchemaForm
from .models import Column, DataSet, Schema
from .tasks import create_csv
from django.http import JsonResponse


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schemas'] = Schema.objects.filter(user=self.request.user)
        return context


class SchemaEditView(LoginRequiredMixin, UpdateView):
    model = Schema
    fields = ('title', 'column_separator', 'string_character')
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse_lazy('column_list', kwargs={'schema_id': self.object.id})


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    model = Schema
    template_name_suffix = '_delete'
    success_url = reverse_lazy('schema_list')

@login_required
def create_schema(request):
    form = SchemaForm()
    if request.method == 'POST':
        form = SchemaForm(request.POST)
        if form.is_valid():
            schema = Schema.objects.create(
                title=form.cleaned_data['title'], column_separator=form.cleaned_data['column_separator'], string_character=form.cleaned_data['string_character'], user=request.user)
            schema.save()
            print(schema.pk)
            return redirect('column_create', args=schema.pk)
        else:
            form = SchemaForm()

    context = {
        'form': form,
    }

    return render(request, 'fakecsv/schema_create.html', context)

@login_required
def column_create(request, args):
    schema_id = args
    schema = Schema.objects.get(pk=schema_id)

    form = ColumnForm()
    column = Column.objects.filter(schema=schema_id)
    if request.method == 'POST':
        form = ColumnForm(request.POST)
        if form.is_valid():
            if request.POST['column_type'] == 'Integer':
                column = Column.objects.create(name=form.cleaned_data['name'], column_type=form.cleaned_data['column_type'],
                                               start_value=form.cleaned_data['start_value'], end_value=form.cleaned_data['end_value'], order=form.cleaned_data['order'], schema=schema)
                column.save()
                return redirect('column_create', args=schema.pk)

            else:
                column = Column.objects.create(name=form.cleaned_data['name'], column_type=form.cleaned_data['column_type'],
                                               order=form.cleaned_data['order'], schema=schema)
                column.save()
                return redirect('column_create', args=schema.pk)

    context = {
        'form': form,
        'columns': column,
    }

    return render(request, 'fakecsv/column_create.html', context)

@login_required
def column_list(request, schema_id):
    schema_id = schema_id
    schema = Schema.objects.get(pk=schema_id)
    column = Column.objects.filter(schema=schema_id)

    context = {
        'columns': column,
        'schema': schema,
    }

    return render(request, 'fakecsv/column_list.html', context)


class ColumnEditView(LoginRequiredMixin, UpdateView):
    model = Column
    fields = ('name', 'column_type', 'start_value', 'end_value', 'order')
    template_name_suffix = '_update'
    success_url = reverse_lazy('schema_list')


class ColumnDeleteView(LoginRequiredMixin, DeleteView):
    model = Column
    template_name_suffix = '_delete'
    success_url = reverse_lazy('schema_list')


class DatasetsListView(LoginRequiredMixin, ListView):
    model = DataSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datasets'] = DataSet.objects.filter(user=self.request.user)
        return context


@login_required
def create_dataset(request):
    if request.method == 'POST':
        rows = int(request.POST.get('rows'))
        schemas = Schema.objects.filter(user=request.user)
        lst = []
        for schema in schemas:
            dataset = DataSet.objects.create(user=request.user, schema=schema)
            lst.append(dataset)
            create_csv.apply_async(args=[dataset.id, schema.id, rows])
        return redirect('dataset_list')
    return redirect('dataset_list')


def get_datasets(request):
    datasets = DataSet.objects.all().values('id', 'status')
    return JsonResponse({'datasets': list(datasets)})
    