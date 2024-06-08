from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from orders.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'email',
            'name',
            'phone',
            'zipcode',
            'address',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # 验证电话号码格式是否正确
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError(_('請輸入有效的手機號碼。'))
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        # 验证电子邮件地址格式是否正确
        if not email or '@' not in email:
            raise ValidationError(_('Please enter a valid email address.'))
        return email