from decouple import config

merchat_id = config("MERCHANT_ID")
merchat_secret = config("MERCHANT_SECRET")
payment_testing_mode = config("PAYMENT_TESTING_MODE")
success_url = config("PAYBOX_SUCCES_URL")


class PaymentStatus:
    in_progres = "в обработке"
    paid = "оплачен"
    canceled = "отменен"
    not_paid = "не оплачен"

    @classmethod
    def choices(cls):
        return (
            (cls.in_progres, cls.in_progres),
            (cls.paid, cls.paid),
            (cls.canceled, cls.canceled),
            (cls.not_paid, cls.not_paid),
        )
