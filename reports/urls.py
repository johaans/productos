from django.urls import path

from reports.views import ReportSaleView

urlpatterns = [
    # reports
    path('salida/', ReportSaleView.as_view(), name='sale_report'),
]