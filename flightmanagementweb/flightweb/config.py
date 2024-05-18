import os


class Config:
    VNPAY_TMN_CODE = os.getenv('VNPAY_TMN_CODE', 'E9E58S82')
    VNPAY_HASH_SECRET_KEY = os.getenv('VNPAY_HASH_SECRET_KEY', 'J9ILRBK5TYLIN39413RIOVD4SDW9AWFB')
    VNPAY_PAYMENT_URL = os.getenv('VNPAY_PAYMENT_URL', 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html')
    VNPAY_RETURN_URL = os.getenv('VNPAY_RETURN_URL', 'http://yourdomain.com/payment_return')
