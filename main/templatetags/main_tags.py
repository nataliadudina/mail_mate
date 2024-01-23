from django import template
from blog.models import Article

from main.models import Client

register = template.Library()


# @register.inclusion_tag('main/tag_list.html')
# def show_tags(tag_selected=0):
#     clients = Client.objects.all()
#     tags = clients.tag.distinct()
#     return {'tags': tags, 'tag_selected': tag_selected}
