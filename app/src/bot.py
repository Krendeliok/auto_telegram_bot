from .disp import current_dispatcher as dp
from .handlers import advertisement, admin, owner, general, payments


owner.register_handlers_owner(dp)
admin.register_handlers_admin(dp)
advertisement.register_handlers_advertisement(dp)
general.register_hendlers_general(dp)
payments.register_hendlers_payment(dp)
