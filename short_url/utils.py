import random
import string

def generate_random_code(instance, items=string.ascii_lowercase+string.digits):
    new_code = ''.join(random.choice(items) for i in range(6))
    klass = instance.__class__
    qs_exists = klass.objects.filter(shortcode=new_code).exists()
    if qs_exists:
        return generate_random_code(instance)
    return new_code

