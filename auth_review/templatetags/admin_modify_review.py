import sys

from django.template.context import Context
from django import template
from django.contrib.admin.templatetags.base import InclusionAdminNode

register = template.Library()

def submit_row_network(context):
    ctx = Context(context)
    ctx.update(
        {
            "login_twitter": True
        }
    )
    return ctx

@register.tag(name="submit_row_network")
def submit_row_tag(parser, token):
    return InclusionAdminNode(
        parser, token, func=submit_row_network, template_name="submit_line_network.html"
    )
