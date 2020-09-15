from .logger import error
from .logger import event

from .storage import init

# login
from .storage import get_last_login
from .storage import set_last_login

# cash in
from .storage import get_cash_in_logs
from .storage import add_cash_in_log
from .storage import set_step_cash_in_log
from .storage import update_cash_in_log

# cash out
from .storage import add_cash_out_log
from .storage import get_cash_out_logs
from .storage import set_step_cash_out_log

# event
from .storage import get_events
from .storage import add_event

# notes
from .storage import get_balance
from .storage import get_note_count
from .storage import get_notes
from .storage import set_note_count
from .storage import reset_notes_count