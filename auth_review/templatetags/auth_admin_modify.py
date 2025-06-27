from django import template
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.contrib.admin.templatetags.admin_modify import submit_row
register = template.Library()

def submit_row_network(context):
    ctx = submit_row(context)
    login_twitter = context.get("login_twitter", False)
    from ReviewApp.settings import env

    ctx.update({
        'login_twitter': login_twitter,
        'api_client_id_google' : env("API_KEY_CLIENT_GOOGLE")
    })

    return ctx

@register.tag(name="submit_row_social")
def submit_row_tag(parser, token):
    return InclusionAdminNode(
        parser, token, func=submit_row_network, template_name="submit_line_social.html"
    )
