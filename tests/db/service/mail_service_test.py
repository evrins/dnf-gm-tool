from dnfpkgtool.db.entity.mail_form_item import ItemType, MailFormItem
from dnfpkgtool.db.service.mail_service import MailService


def test_send_stackable_mail_with_multi_mail():
    sender = 'evrins'
    msg = 'test message'
    character_no = 8

    mail_item = MailFormItem(
        item_type=ItemType.Stackable,
        item_id=1250,
        num=9500,
        gold=2460,
    )

    svc = MailService()
    svc.send_stackable_mail(sender, msg, character_no, mail_item)


def test_send_stackable_mail():
    sender = 'evrins'
    msg = 'test message'
    character_no = 8

    mail_item = MailFormItem(
        item_type=ItemType.Stackable,
        item_id=1250,
        num=100,
        gold=2460,
    )

    svc = MailService()
    svc.send_stackable_mail(sender, msg, character_no, mail_item)


def test_send_creature_mail_for_egg():
    sender = 'evrins'
    msg = 'test message'
    character_no = 8

    mail_item = MailFormItem(
        item_type=ItemType.Creature,
        item_id=63015,
        sub_type=1,
    )

    svc = MailService()
    svc.send_creature_mail(sender, msg, character_no, mail_item)


def test_send_creature_mail():
    sender = 'evrins'
    msg = 'test message'
    character_no = 8

    mail_item = MailFormItem(
        item_type=ItemType.Creature,
        item_id=63012,
        sub_type=0,
    )

    svc = MailService()
    svc.send_creature_mail(sender, msg, character_no, mail_item)


def test_send_avatar_mail():
    sender = 'evrins'
    msg = 'test message'
    character_no = 8

    mail_item = MailFormItem(
        item_type=ItemType.Avatar,
        item_id=101600007,
    )

    svc = MailService()
    svc.send_avatar_mail(sender, msg, character_no, mail_item)
