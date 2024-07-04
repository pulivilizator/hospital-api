from slugify import slugify
from uuid import uuid4


def unique_slug_generator(instance, slug_field, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(slug_field)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f'{slug}-{str(uuid4())[:8]}'
        return unique_slug_generator(instance, slug_field=slug_field, new_slug=new_slug)
    print(slug)
    return slug
