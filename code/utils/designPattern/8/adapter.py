from abc import ABCMeta, abstractmethod


class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self, money):
        pass


class AliPay(Payment):
    def pay(self, money):
        print("支付宝支付%d元." % money)


class WechatPay(Payment):
    def pay(self, money):
        print("微信支付%d元。" % money)


class BankPay:
    def cost(self, money):
        print("银联支付%d元。" % money)


# # 类适配器
# """
# 将BankPay原先不兼容的cost()接口适配到pay()接口
# """
# class NewBankPay(Payment, BankPay):
#     def pay(self, money):
#         self.cost(money)
#
#
# p = NewBankPay()
# p.pay(100)

class ApplePay:
    def cost(self, money):
        print("苹果支付%d元。" % money)


# 对象适配器
"""
通过组合，将两个不适配的类适配到pay接口
"""
class PaymentAdapter(Payment):
    def __init__(self, payment):
        self.payment = payment

    def pay(self, money):
        self.payment.cost(money)


p = PaymentAdapter(BankPay())
p.pay(100)



