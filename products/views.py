from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from products.models import Product,ProductCategory
from django.http import JsonResponse

class HomeView(TemplateView):
    template_name = "products/home.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        left_product_categories = ProductCategory.objects.all()[0:2]
        right_product_categories = ProductCategory.objects.all()[2:3]
        right_product_category = right_product_categories.first() if right_product_categories else None
        context = self.get_context_data(**kwargs)
        context['items'] = products
        context['left_product_categories'] = left_product_categories
        context['right_product_category'] = right_product_category
        return self.render_to_response(context)
# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'items'
    paginate_by = 10
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'item'

def search_orders(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        # 在這裡通過搜尋資料庫，獲取相應的訂單數據，這裡僅為示例
        # 假設你已經定義了一個 Order 模型
        # orders = Order.objects.filter(phone=phone, email=email)

        # 為了示例，這裡直接返回一些假數據
        orders = [{'id': 1, 'product': 'Product A', 'quantity': 2}, {'id': 2, 'product': 'Product B', 'quantity': 1}]

        return JsonResponse({'orders': orders})
    return JsonResponse({'error': 'Invalid request method'})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'item': product,
    }
    return render(request, 'products/detail.html', context)