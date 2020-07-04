class game:
    def __init__(self):
        pass


class my_class:
    def __init__(self):
        self.attr = 'x'

class my_class2:
    attr = 'x'

y = my_class
z = my_class2

print(y.attr)
print(z.attr)