from django import forms
from blog.models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        # fields设置绑定到forms的 exclude设置不绑定的
        exclude = ("id", "Weights", "is_publish", )
