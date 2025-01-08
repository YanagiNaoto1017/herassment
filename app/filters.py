import django_filters
from .models import Users  # または該当するモデル（例えば、User）
from django.db.models import Q

class UserFilter(django_filters.FilterSet):
    # 企業名の選択肢を動的に取得する
    company = django_filters.ModelChoiceFilter(
        queryset=Users.objects.values_list('company_name', flat=True).distinct(),  # 企業名をリスト化
        label='企業名',
        empty_label='すべての企業'  # デフォルトの選択肢
    )

    class Meta:
        model = Users  # User または該当するモデル
        fields = ['company']
