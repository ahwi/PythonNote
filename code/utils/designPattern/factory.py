from abc import ABCMeta, abstractmethod


# 接口
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self, money):
        pass


class AliPay(Payment):
    def __init__(self, use_huabei=False):
        self.use_huabei = use_huabei

    def pay(self, money):
        if self.use_huabei:
            print("支付宝花呗支付%d元." % money)
        else:
            print("支付宝余额支付%d元." % money)


class WechatPay(Payment):
    def pay(self, money):
        print("微信支付%d元。" % money)


class PaymentFactory:
    def create_payment(self, method):
        if method == 'aliPay':
            return AliPay()
        elif method == 'wechat':
            return WechatPay()
        elif method == 'huabei':
            return AliPay(use_huabei=True)
        else:
            raise TypeError("No such payment named %s" % method)


# client
pf = PaymentFactory()
p = pf.create_payment('aliPay')
p = pf.create_payment('huabei')
p.pay(100)
