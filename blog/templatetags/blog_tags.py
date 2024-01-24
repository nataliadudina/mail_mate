from django import template


# Creates a new instance of template library
register = template.Library()


# Returns the URL of the image field if it exists, otherwise — a default image path
@register.simple_tag()
def imagepath_tag(image_field):
    if image_field:
        return image_field.url
    return '/media/images/blog/default.jpg'
