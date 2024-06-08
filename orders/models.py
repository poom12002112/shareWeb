from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Order(models.Model):
    '''
    訂單
    '''
    order_id = models.CharField(_('Order Id'), max_length=20)
    email = models.EmailField('信箱', max_length=255)
    product = models.ManyToManyField('products.Product', related_name='order_set', through='products.RelationalProduct')
    name = models.CharField(_('姓名'), max_length=50)
    phone = models.CharField(_('電話'), max_length=50)
    zipcode = models.CharField(_('郵遞區號'), max_length=50)
    address = models.CharField(_('地址'), max_length=255)
    total = models.PositiveIntegerField(_('總計'), default=0)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True)
    product_names = models.TextField(blank=True, null=True, verbose_name='商品名稱')
    status = models.CharField(
        _('訂單狀態'), 
        max_length=100, 
        choices=(("未付款", _("未付款")), ("付款失敗", _("付款失敗")), ("付款成功", _("付款成功")),("取消", _("取消"))), 
        default="未付款"
    )
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_id:
            last_order_id = self.__class__.objects.last().id if self.__class__.objects.last() else 0
            new_order_id = max(last_order_id + 1, 500)
            self.order_id = f'ORDER{self.id + 500:08}'
            super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = '訂單'
        verbose_name_plural = '訂單'

    def __str__(self):
        return f'{self.order_id}'