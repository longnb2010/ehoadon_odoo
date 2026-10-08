# -*- coding: utf-8 -*-

LEGACY_MODULE = 'vms_ehoadon'
# What vms_ehoadon still owns after the split: the prescription layer.
LEGACY_KEEP_PATTERN = '%prescription_order%'
LEGACY_KEEP_NAMES = (
    'view_stay_order_form_inherit_ehoadon',
    'view_vaccination_order_form_inherit_ehoadon',
    'view_grooming_order_form_inherit_ehoadon',
)
LEGACY_RENAMED = {
    'module_category_vms_ehoadon': 'module_category_ehoadon',
}


def pre_init_hook(cr):
    """Adopt core records from a pre-split vms_ehoadon install.

    Before the split vms_ehoadon owned the eHoaDon models, groups, ACLs,
    menus and views. Moving their external ids to ``ehoadon`` before it loads
    makes the install update those records in place, so group membership,
    config, templates and logs survive instead of being recreated/deleted.
    """
    cr.execute(
        "SELECT 1 FROM ir_model_data WHERE module = %s AND model = 'res.groups' LIMIT 1",
        (LEGACY_MODULE,),
    )
    if not cr.fetchone():
        return
    cr.execute(
        """
        UPDATE ir_model_data SET module = 'ehoadon'
         WHERE module = %s AND name NOT LIKE %s AND name NOT IN %s
        """,
        (LEGACY_MODULE, LEGACY_KEEP_PATTERN, LEGACY_KEEP_NAMES),
    )
    for old_name, new_name in LEGACY_RENAMED.items():
        cr.execute(
            "UPDATE ir_model_data SET name = %s WHERE module = 'ehoadon' AND name = %s",
            (new_name, old_name),
        )
    # SQL constraints / m2m tables are owned by module id, used on uninstall.
    for table in ('ir_model_constraint', 'ir_model_relation'):
        cr.execute(
            """
            UPDATE {table} t SET module = new.id
              FROM ir_module_module old, ir_module_module new, ir_model m
             WHERE old.name = %s AND new.name = 'ehoadon'
               AND t.module = old.id AND t.model = m.id AND m.model LIKE 'ehoadon.%%'
            """.format(table=table),
            (LEGACY_MODULE,),
        )
