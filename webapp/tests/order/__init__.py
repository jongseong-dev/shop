class StripeMock:
    def __init__(self, **kwargs):
        self.payment_intent = kwargs.get("payment_intent", "pi_123")
        self.client_reference_id = kwargs.get("client_reference_id", 1)
        self.mode = kwargs.get("mode", "payment")
        self.payment_status = kwargs.get("payment_status", "paid")
