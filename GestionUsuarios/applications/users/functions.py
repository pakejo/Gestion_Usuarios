import random
import string


# Extra functions for users app
def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choices(chars) for _ in range(size))
