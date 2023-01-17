# 简单工厂模式

from abc import ABCMeta, abstractmethod


class Pay(metaclass=ABCMeta):

    @abstractmethod
    def pay(self, money):
        pass


class AliPay(Pay):

    def pay(self, money):
        print("支付宝支付%d元" % money)


class WechatPay(Pay):

    def pay(self, money):
        print("微信支付%d元" % money)


class PayFactory():
    def create_payment(self, method):
        if method == "aliPay":
            return AliPay()
        elif method == "wechatPay":
            return WechatPay()
        else:
            raise TypeError("No such payment named %s" % method)


# client
factory = PayFactory()
pay = factory.create_payment("aliPay")
pay.pay(100)
