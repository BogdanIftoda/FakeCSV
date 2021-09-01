from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (ColumnDeleteView, ColumnEditView, DatasetsListView,
                    SchemaDeleteView, SchemaEditView, SchemaListView,
                    column_create, create_schema, column_list, create_dataset, get_datasets)
urlpatterns = [
    path('login/', LoginView.as_view(template_name='fakecsv/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='fakecsv/logout.html'), name='logout'),
    path('', SchemaListView.as_view(), name='schema_list'),
    path('schema_create/', create_schema, name='schema_create'),
    path('schema_update/<int:pk>/', SchemaEditView.as_view(), name='schema_update'),
    path('schema_delete/<int:pk>/',
         SchemaDeleteView.as_view(), name='schema_delete'),
    path('column_create/<int:args>/', column_create, name='column_create'),
    path('column_update/<int:pk>/', ColumnEditView.as_view(), name='column_update'),
    path('column_delete/<int:pk>/',
         ColumnDeleteView.as_view(), name='column_delete'),
    path('column_list/<int:schema_id>/', column_list, name='column_list'),
    path('get_datasets/', get_datasets, name='get_datasets'),
    path('dataset_list/', DatasetsListView.as_view(), name='dataset_list'),
    path('dataset_create/', create_dataset, name='dataset_create'),
]
