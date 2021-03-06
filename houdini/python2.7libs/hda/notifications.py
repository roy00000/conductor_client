"""Provide UI to specify what events to notify users of.

Currently only email notifications.

"""

import re

# Very simple loose email regex, matches 1 email address.
SIMPLE_EMAIL_RE = re.compile(r"^\S+@\S+$")


def validate_emails(node, **_):
    """Emails must all be somewhat valid.

    Split the list of emails and loop through. Disable
    `valid` tickmark if any matches fail.

    """

    val = node.parm("email_addresses").eval().strip(',').strip()
    result = bool(val)
    for address in [x.strip() for x in val.split(',')]:
        if not SIMPLE_EMAIL_RE.match(address):
            result = False
            break
    node.parm("email_valid").set(result)


def email_hook_changed(node, **_):
    """If no email hooks selected then dim out the email field.

    Get the child toggles of the hooks folder dynamically
    rather than list them explicitly. In this way, other
    hooks can be added with minimum fuss.

    """
    result = 0
    template = node.type().definition().parmTemplateGroup().find('hooks')
    hooks = [p.name() for p in template.parmTemplates()
             if p.type().name() == "Toggle"]
    for hook in hooks:
        if node.parm(hook).eval():
            result = 1
            break
    node.parm("do_email").set(result)
