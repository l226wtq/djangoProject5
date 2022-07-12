from django.forms import ModelForm
from django.forms import inlineformset_factory

from app01.models import sqlStatementDocument, sqlSingleStatmentList


class newSqlForm(ModelForm):
    class Meta:
        model = sqlStatementDocument
        fields = "__all__"


IngredientFormSet = inlineformset_factory(sqlStatementDocument, sqlSingleStatmentList, can_delete=False)
