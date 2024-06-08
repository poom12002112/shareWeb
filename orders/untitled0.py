import base64
import pickle

# 從 cookie 中獲取購物車信息字符串
cart_str = "gASVQQAAAAAAAAB9lChLBX2UjAVjb3VudJRLAXNLBH2UjAVjb3VudJRLAXNLA32UjAVjb3VudJRLAXNLAn2UjAVjb3VudJRLAXN1Lg=="

# base64 解碼
cart_bytes = base64.b64decode(cart_str.encode())

# pickle 加載
cart_dict = pickle.loads(cart_bytes)

# 打印購物車信息
print(cart_dict)