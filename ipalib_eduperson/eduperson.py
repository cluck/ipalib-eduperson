# -*- coding: utf-8 -*-

import datetime
import re

from ipalib import _
from ipalib import errors, output
from ipalib.parameters import Str
from ipalib.plugable import Registry
from ipalib.plugins import user
from ipalib.plugins.baseldap import (
        LDAPQuery,
        pkey_to_value,
        add_missing_object_class,
    )
from ipalib.plugins.internal import i18n_messages


# No other way to do this?:
i18n_messages.messages['actions'].update({
        'user_addeduperson': _("Enable eduPerson"),
        'user_addeduperson_confirm': _("Enable eduPerson?"),
        'user_addeduperson_success': _("eduPerson Enabled"),
        'user_deleduperson': _("Disable eduPerson"),
        'user_deleduperson_confirm': _("Disable eduPerson?"),
        'user_deleduperson_success': _("eduPerson Disabled"),
    })


user.user.takes_params += (
    Str('edupersonaffiliation*',
        cli_name='ep_affiliation',
        label=_('eduPerson Affiliation'),
    ),
    Str('edupersonentitlement*',
        cli_name='ep_entitlement',
        label=_('eduPerson Entitlement'),
    ),
    Str('edupersonnickname*',
        cli_name='ep_nickname',
        label=_('eduPerson Nickname'),
    ),
    Str('edupersonorgdn?',
        cli_name='ep_o_dn',
        label=_('eduPerson Organization DN'),
    ),
    Str('edupersonorgunitdn?',
        cli_name='ep_ou_dn',
        label=_('eduPerson Organizational Unit DN'),
    ),
    Str('edupersonprimaryaffiliation?',
        cli_name='ep_primary_affiliation',
        label=_('eduPerson Primary Affiliation'),
    ),
    Str('edupersonprincipalname?',
        cli_name='ep_pn',
        label=_('eduPerson Principal Name'),
    ),
    Str('edupersonprimaryorgunit?',
        cli_name='ep_primary_ou',
        label=_('eduPerson Primary Organizational Unit'),
    ),
    Str('edupersontargetedid*',
        cli_name='ep_tgt_id',
        label=_('eduPerson Targeted ID'),
    ),
    Str('edupersonassurance*',
        cli_name='ep_assurance',
        label=_('eduPerson Assurance'),
    ),
)

ATTRIBUTES = [
    'eduPersonAffiliation',
    'eduPersonAssurance',
    'eduPersonEntitlement',
    'eduPersonNickname',
    'eduPersonOrgDN',
    'eduPersonOrgUnitDN',
    'eduPersonPrimaryAffiliation',
    'eduPersonPrimaryOrgUnit',
    'eduPersonPrincipalName',
    'eduPersonTargetedID',
]

KNOWN_AFFILIATION = (
    'guest',
    'student',
    'staff',
    'virtual',
)

register = Registry()


def useradd_precallback(self, ldap, dn, entry, attrs_list, *keys, **options):
    try:
        objectclass = entry['objectclass']
    except KeyError:
        objectclass = entry['objectclass'] = []
        if 'objectclass' not in attrs_list:
            attrs_list.append('objectclass')
    if any(((att.lower() in entry) for att in ATTRIBUTES)):
        if 'eduPerson' not in objectclass:
            objectclass.append('eduPerson')
    return dn

user.user_add.register_pre_callback(useradd_precallback)



def usermod_precallback(self, ldap, dn, entry, attrs_list, *keys, **options):
    if any(((att.lower() in entry) for att in ATTRIBUTES)):
        entry.update(add_missing_object_class(ldap, 'eduPerson', dn, update=False))
    return dn

user.user_mod.register_pre_callback(usermod_precallback)


@register()
class user_addeduperson(LDAPQuery):
    __doc__ = _('Make user an eduPerson.')

    has_output = output.standard_value
    msg_summary = _('eduPerson enabled on "%(value)s"')

    def execute(self, *keys, **options):
        dn = self.obj.get_dn(*keys, **options)
        entry = self.obj.backend.get_entry(dn, ['objectclass'])

        if 'eduPerson' not in entry['objectclass']:
            entry['objectclass'].append('eduPerson')

        self.obj.backend.update_entry(entry)

        return dict(
            result=True,
            value=pkey_to_value(keys[0], options),
        )


@register()
class user_deleduperson(LDAPQuery):
    __doc__ = _('Remove eduPerson attributes from users.')

    has_output = output.standard_value
    msg_summary = _('eduPerson disabled on "%(value)s"')

    def execute(self, *keys, **options):
        dn = self.obj.get_dn(*keys, **options)
        entry = self.obj.backend.get_entry(dn, ['objectclass'] + ATTRIBUTES)

        while 'eduPerson' in entry['objectclass']:
            entry['objectclass'].remove('eduPerson')

        for att in ATTRIBUTES:
            try:
                del entry[att]
            except KeyError:
                pass

        self.obj.backend.update_entry(entry)

        return dict(
            result=True,
            value=pkey_to_value(keys[0], options),
        )

