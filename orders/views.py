from django.shortcuts import render
from django.views.generic import View, TemplateView,FormView
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse,Http404
from products.models import Product,ProductOption
import base64
import pickle
from .forms import OrderForm  # 确保你导入了正确的表单类
from .models import Order  # 确保你导入了正确的模型类
from .ecpay_payment_sdk import ECPayPaymentSdk
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt,csrf_protect,requires_csrf_token
from products.models import RelationalProduct
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.sessions.models import Session
from django.db.models import Max
from django.urls import reverse
import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder



class AddCartView(View):
    def get(self, request, *args, **kwargs):
        productoption_id = self.kwargs.get('size_id', '')
        cart_str = request.COOKIES.get('cart', '')
        if productoption_id:
            if cart_str:
                cart_bytes = cart_str.encode()
                cart_bytes = base64.b64decode(cart_bytes)
                cart_dict = pickle.loads(cart_bytes)
            else:
                cart_dict = {}
            if productoption_id in cart_dict:
                cart_dict[productoption_id]['count'] += 1
            else:
                cart_dict[productoption_id] = {
                    'count': 1,
                }
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
        context = {}
        context["status"] = 200
        response = JsonResponse(context)
        response.set_cookie("cart", cart_str)
        return response

    def post(self, request, *args, **kwargs):
        productoption_id = request.POST.get('size_id', '')
        cart_str = request.COOKIES.get('cart', '')
        if productoption_id:
            if cart_str:
                cart_bytes = cart_str.encode()
                cart_bytes = base64.b64decode(cart_bytes)
                cart_dict = pickle.loads(cart_bytes)
            else:
                cart_dict = {}
            if productoption_id in cart_dict:
                cart_dict[productoption_id]['count'] += 1
            else:
                cart_dict[productoption_id] = {
                    'count': 1,
                }
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
        context = {}
        context["status"] = 200
        response = JsonResponse(context)
        response.set_cookie("cart", cart_str)
        return response

class DeleteCartView(View):

    def get(self, request, *args, **kwargs):
        productoption_id = self.kwargs.get('size_id', '')
        cart_str = request.COOKIES.get('cart', '')
        if productoption_id:
            if cart_str:
                cart_bytes = cart_str.encode()
                cart_bytes = base64.b64decode(cart_bytes)
                cart_dict = pickle.loads(cart_bytes)
            else:
                cart_dict = {}
            if productoption_id in cart_dict:
                del cart_dict[productoption_id]
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
        context = {}
        context["status"] = 200
        response = JsonResponse(context)
        response.set_cookie("cart", cart_str)
        return response
    def post(self, request, *args, **kwargs):
        productoption_id = request.POST.get('size_id', '')  # 假设你的前端会发送一个名为 'size_id' 的参数
        cart_str = request.COOKIES.get('cart', '')
        if productoption_id:
            if cart_str:
                cart_bytes = cart_str.encode()
                cart_bytes = base64.b64decode(cart_bytes)
                cart_dict = pickle.loads(cart_bytes)
            else:
                cart_dict = {}
            if productoption_id in cart_dict:
                del cart_dict[productoption_id]
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
        context = {}
        context["status"] = 200
        response = JsonResponse(context)
        response.set_cookie("cart", cart_str)
        return response

class CartView(TemplateView):
    template_name = "orders/cart.html"

    def get(self, request, *args, **kwargs):
        cart_str = request.COOKIES.get('cart', '')
        product_dict = {}
        total = 0
        if cart_str:
            cart_bytes = cart_str.encode()
            cart_bytes = base64.b64decode(cart_bytes)
            cart_dict = pickle.loads(cart_bytes)
            for productoption_id, product_data in cart_dict.items():
                product_option = ProductOption.objects.filter(id=productoption_id).first()
                if product_option:
                    product = product_option.product
                    size = product_option.size
                    price = product_option.price
                    count = product_data['count']
                    product_dict[productoption_id] = {
                        "product": product,
                        "size": size,
                        "price":price,
                        "count": count,
                        "total_price": price * count
                    }
                    total += int(product_data['count']) * int(price)
        context = self.get_context_data(**kwargs)
        context["product_dict"] = product_dict
        context["total"] = total
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        cart_str = request.COOKIES.get('cart', '')
        product_dict = {}
        if cart_str:
            cart_bytes = cart_str.encode()
            cart_bytes = base64.b64decode(cart_bytes)
            cart_dict = pickle.loads(cart_bytes)
            for productoption_id in cart_dict:
                if product := ProductOption.objects.filter(id=productoption_id):
                    product_dict[productoption_id] = {
                        "product": product.first(),
                        "count": cart_dict[productoption_id]['count']
                    }

        for product_id, item in product_dict.items():
            quantity_key = 'quantity_' + str(product_id)
            if quantity_key in request.POST:
                quantity = int(request.POST[quantity_key])
                item['count'] = quantity

        # 更新购物车信息
        updated_cart_dict = {productoption_id: {"count": item['count']} for productoption_id, item in product_dict.items()}
        updated_cart_bytes = pickle.dumps(updated_cart_dict)
        updated_cart_str = base64.b64encode(updated_cart_bytes).decode()
        response = HttpResponseRedirect(reverse('orders:cart'))
        response.set_cookie('cart', updated_cart_str)

        return response


class CheckoutView(FormView):
    template_name = "orders/checkout.html"
    form_class = OrderForm
    success_url = 'orders/confirmation.html'

    def get_cart_cookie(self, request):
        cart_str = request.COOKIES.get('cart', '')
        cart_dict = {}
        if cart_str:
            cart_bytes = cart_str.encode()
            cart_bytes = base64.b64decode(cart_bytes)
            cart_dict = pickle.loads(cart_bytes)
        return cart_dict

    def get(self, request, *args, **kwargs):
        cart_dict = self.get_cart_cookie(request)
        product_dict = {}
        total = 0
        if cart_dict:
            for productoption_id, product_data in cart_dict.items():
                product_option = ProductOption.objects.filter(id=productoption_id).first()
                if product_option:
                    product = product_option.product
                    size = product_option.size
                    price = product_option.price
                    count = product_data['count']
                    product_dict[productoption_id] = {
                        "product": {
                            'id': product.id,
                            'name': product.name,
                            'size': size,
                            'price': float(price),  # 將 Decimal 轉換為 float
                            'image_url': product.product_image_set.first().image.url if product.product_image_set.first() else None,
                        },
                        "count": count,
                        "total_price": float(price) * count  # 將 Decimal 轉換為 float
                    }
                    total += float(price) * count  # 將 Decimal 轉換為 float
            request.session['product_dict'] = product_dict
            request.session['total'] = total
        else:
            request.session.pop('product_dict', None)
            request.session.pop('total', None)
        context = self.get_context_data(**kwargs)
        context["product_dict"] = product_dict
        context["total"] = total
        return self.render_to_response(context)

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        cart_dict = self.get_cart_cookie(self.request)
        
        if cart_dict:
            product_details = []
            total = 0
            for productoption_id, product_data in cart_dict.items():
                product_option = ProductOption.objects.filter(id=productoption_id).first()
                if product_option:
                    product = product_option.product
                    product_details.append(f"{product.name} ({product_option.size}) ({product_data['count']})")
                    total += float(product_data['count']) * float(product_option.price)
                    
            self.object.total = total
            self.object.product_names = ', '.join(product_details)
            self.object.save()
            
            for productoption_id, product_data in cart_dict.items():
                product_option = ProductOption.objects.filter(id=productoption_id).first()
                if product_option:
                    product = product_option.product
                    RelationalProduct.objects.create(order=self.object, product=product, number=product_data['count'])
        
        self.request.session.pop('product_dict', None)
        self.request.session.pop('total', None)
        
        context = self.get_context_data(form=form)
        context['order_id'] = self.object.order_id
        return render(self.request, self.success_url, context=context)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        product_dict = self.request.session.get('product_dict', {})
        total = self.request.session.get('total', 0)
        context = self.get_context_data(form=form, product_dict=product_dict, total=total)
        return self.render_to_response(context)




    
class ECPayView(TemplateView):
    template_name = "orders/ecpay.html"

    def post(self, request, *args, **kwargs):
        scheme = request.is_secure() and "https" or "http"
        domain = request.META['HTTP_HOST']

        order_id = request.POST.get("order_id")
        order = Order.objects.get(order_id=order_id)
        product_list = "#".join([product.name for product in order.product.all()])
        order_params = {
            'MerchantTradeNo': order.order_id,
            'StoreID': '',
            'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            'PaymentType': 'aio',
            'TotalAmount': order.total,
            'TradeDesc': order.order_id,
            'ItemName': product_list,
            'ReturnURL': f'{scheme}://{domain}/orders/return/',  # ReturnURL
            'ChoosePayment': 'ALL',
            'ClientBackURL': f'{scheme}://{domain}/orders/checkout/',  # 返回商店按鈕
            'ItemURL': f'{scheme}://{domain}/products/list/',  # 商品銷售網址
            'Remark': '交易備註',
            'ChooseSubPayment': '',
            'OrderResultURL': f'{scheme}://{domain}/orders/orderresult/',  # 付款完成後
            'NeedExtraPaidInfo': 'Y',
            'DeviceSource': '',
            'IgnorePayment': '',
            'PlatformID': '',
            'InvoiceMark': 'N',
            'CustomField1': '',
            'CustomField2': '',
            'CustomField3': '',
            'CustomField4': '',
            'EncryptType': 1,
        }
        # 建立實體
        ecpay_payment_sdk = ECPayPaymentSdk(
            MerchantID='3002607',
            HashKey='pwFHCqoQZGmho4w6',
            HashIV='EkRm7iFT261dpevs'
        )
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        ecpay_form = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        context = self.get_context_data(**kwargs)
        context['ecpay_form'] = ecpay_form
        return self.render_to_response(context)
    
class OrderSuccessView(TemplateView):
    template_name = "orders/order_success.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class ReturnView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ecpay_payment_sdk = ECPayPaymentSdk(
            MerchantID='3002607',
            HashKey='pwFHCqoQZGmho4w6',
            HashIV='EkRm7iFT261dpevs'
        )
        res = request.POST.dict()
        back_check_mac_value = request.POST.get('CheckMacValue')
        check_mac_value = ecpay_payment_sdk.generate_check_value(res)
        if check_mac_value == back_check_mac_value:
            response = HttpResponse('1|OK')
            clear_cart(response)
            return response
        return HttpResponse('0|Fail')
    
class OrderResultView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderResultView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):

        ecpay_payment_sdk = ECPayPaymentSdk(
            MerchantID='3002607',
            HashKey='pwFHCqoQZGmho4w6',
            HashIV='EkRm7iFT261dpevs'
        )
        res = request.POST.dict()
        back_check_mac_value = request.POST.get('CheckMacValue')
        order_id = request.POST.get('MerchantTradeNo')
        rtnmsg = request.POST.get('RtnMsg')
        rtncode = request.POST.get('RtnCode')
        check_mac_value = ecpay_payment_sdk.generate_check_value(res)
        if check_mac_value == back_check_mac_value and rtnmsg == 'Succeeded' and rtncode == '1':
            order = Order.objects.get(order_id=order_id)
            order.status = '付款成功'
            order.save()
            response = HttpResponseRedirect('/orders/order_success/')
            clear_cart(response)
            return response
        else:
            order = Order.objects.get(order_id=order_id)
            order.status = '付款失敗'
            order.save()
            return HttpResponseRedirect('/orders/order_fail/')

class OrderFailView(TemplateView):
    template_name = "orders/order_fail.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
from django.http import JsonResponse
from django.views import View

class SearchOrders(View):
    
    def post(self, request):
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        # 在这里通过搜索数据库，获取相应的订单数据，这里仅为示例
        # 假设你已经定义了一个 Order 模型
        # orders = Order.objects.filter(phone=phone, email=email)

        # 为了示例，这里直接返回一些假数据
        orders = [{'id': 1, 'product': 'Product A', 'quantity': 2}, {'id': 2, 'product': 'Product B', 'quantity': 1}]

        return JsonResponse({'orders': orders})


class IndexView(TemplateView):
    template_name = "orders/index.html"

    def get(self, request, *args, **kwargs):
        # 渲染初始页面，这里可能不需要任何逻辑
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # 获取电话和电子邮件
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if phone and email:
            # 如果电话和电子邮件都存在，则认为成功
            success = True
            status='付款成功'
            # 获取符合条件的订单内容，并按订单编号降序排列
            matching_orders = Order.objects.filter(phone=phone, email=email, status=status).order_by('-id')
            if matching_orders.exists():
                # 找到符合条件的订单
                orders = matching_orders.values()
            else:
                # 没有找到符合条件的订单
                orders = None

        else:
            success = False
            orders = None

        context = self.get_context_data(**kwargs)
        context["success"] = success
        context["orders"] = orders
        return self.render_to_response(context)
    
def clear_cart(response):
    response.delete_cookie('cart')


class UpdateCartView(View):
    def post(self, request, *args, **kwargs):
        try:
            productoption_id = request.POST.get('size_id')
            quantity = int(request.POST.get('quantity'))

            cart_str = request.COOKIES.get('cart', '')
            if not cart_str:
                return JsonResponse({'success': False, 'message': '購物車為空'})

            cart_bytes = cart_str.encode()
            cart_bytes = base64.b64decode(cart_bytes)
            cart_dict = pickle.loads(cart_bytes)

            # 更新對應的項目
            if productoption_id in cart_dict:
                cart_dict[productoption_id]['count'] = quantity

            updated_cart_bytes = pickle.dumps(cart_dict)
            updated_cart_str = base64.b64encode(updated_cart_bytes).decode()
            response = JsonResponse({'success': True})
            response.set_cookie('cart', updated_cart_str)
            return response

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

