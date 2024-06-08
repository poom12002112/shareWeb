from django.contrib import admin
from products.models import Product, ProductCategory, ProductImage, ProductOption # 匯入模型
# Register your models here.
class ProductImageInline(admin.TabularInline): # 內嵌管理介面
    model = ProductImage
    fields = ('name', 'image', 'order')
    list_display = ('name', 'category')
    list_filter = ('category',)

class ProductOptionInline(admin.TabularInline):  # 或者使用 admin.StackedInline
    model = ProductOption
    extra = 1  # 額外顯示的一個空白選項表單
    fields = ('size', 'price')  # 顯示尺寸和價格
    
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category__name']
    fields = ('name', 'description', 'category', 'created', 'modified')
    list_display = ('name', 'category')
    list_filter = ('category',)
    autocomplete_fields = ['category']
    readonly_fields = ('created', 'modified')
    inlines = [ProductOptionInline,ProductImageInline]  # 注意這裡的逗號和中括號

class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fields = ('name', 'description', 'created', 'modified')
    list_display = ('name',)
    readonly_fields = ('created', 'modified')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)