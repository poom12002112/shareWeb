from django.contrib import admin

# Register your models here.
from orders.models import Order
from products.models import RelationalProduct

class RelationalProductInline(admin.TabularInline):
    model = RelationalProduct
    verbose_name = '商品名稱'
    extra = 2
    fields = ('get_product_name', 'number')  # 设置要在表单中显示的字段
    readonly_fields = ('get_product_name', 'number')

    def get_product_name(self, instance):
        return instance.product.name

    get_product_name.short_description = '商品名稱'  # 设置表头显示的名称

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    model = Order
    search_fields = ['order_id', 'name']
    fields = ('order_id', 'name', 'email', 'phone', 'zipcode', 'address', 'total', 'status', 'created', 'modified')
    list_display = ('order_id', 'name', 'email', 'total', 'modified')
    list_filter = ('status',)
    readonly_fields = ('order_id', 'name', 'email', 'phone', 'zipcode', 'address', 'total', 'created', 'modified','product_names')
    inlines = [RelationalProductInline,]

admin.site.register(Order, OrderAdmin)