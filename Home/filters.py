import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class CThomeFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="date_created",lookup_expr='gte')  # looks up in date created and gte means greater than or equal to
    # end_date = DateFilter(field_name="date_created", lookup_expr='lte')       #looks up in date created and lte means less than or equal to        note = CharFilter(field_name='note', lookup_expr='icontains')  #icontains means ignore case sensitive data
    rollno=CharFilter(field_name="student")
    class Meta:
        model = Appeal
        fields = ['type']
        #exclude = ['qr_code']  # exculdes these columns and adds above 3 columns

class studentFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="actual_out", lookup_expr='gte')
    end_date = DateFilter(field_name="actual_out", lookup_expr='lte')
    class Meta:
        model=Appeal
        fields=['type']
class lefttodayFilter(django_filters.FilterSet):
    enter_date=DateFilter(field_name="actual_out")
    class Meta:
        model=Appeal
        fields=['branch','year']

class arrivedtodayFilter(django_filters.FilterSet):
    enter_date=DateFilter(field_name="actual_in")
    class Meta:
        model=Appeal
        fields=['branch','year']
class knowstudentstatusFilter(django_filters.FilterSet):
    roll_no=CharFilter(field_name="rollno")