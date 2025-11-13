from PySide6.QtCore import QObject, Signal

from dnfpkgtool.db.entity.mail_submit_item import MailSubmitItem


class GlobalSignals(QObject):
    db_config_changed = Signal()
    pvf_changed = Signal()
    account_id_changed = Signal()
    character_no_changed = Signal()
    submit_mail_form = Signal(MailSubmitItem)
    character_info_changed = Signal()

    def __init__(self):
        super().__init__()


gs = GlobalSignals()
