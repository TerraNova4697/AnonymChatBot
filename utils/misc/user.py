

class User:
    user_id: int
    name: str
    status: str
    partner_id: int
    is_notified: bool = False
    denied_partners: list = [0, ]
