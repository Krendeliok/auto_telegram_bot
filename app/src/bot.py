from .disp import current_dispatcher as dp
from .handlers import advertisement, admin, owner, general


owner.register_handlers_owner(dp)
admin.register_handlers_admin(dp)
advertisement.register_handlers_advertisement(dp)
general.register_hendlers_general(dp)
