import random
import string


def generate_ticket():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
