from knockoutpy.observable import InputValue, ComputedValue

if __name__ == '__main__':
    a = InputValue(5, 'a')

    b = ComputedValue(lambda: a.value * 2, 'b')
    c = ComputedValue(lambda: a.value + 3, 'c')
    d = ComputedValue(lambda: b.value + c.value, 'd')
    e = ComputedValue(lambda: a.value + d.value, 'e')

    print('a = {}'.format(a.value))
    print('b = {}'.format(b.value))
    print('c = {}'.format(c.value))
    print('d = {}'.format(d.value))
    print('e = {}'.format(e.value))

    def print_value(o): 
        print('{} value changed to {}'.format(o.name, o.value))

    a.on_change(print_value)
    b.on_change(print_value)
    c.on_change(print_value)
    d.on_change(print_value)
    e.on_change(print_value)

    a.value = 7

    print('a = {}'.format(a.value))
    print('b = {}'.format(b.value))
    print('c = {}'.format(c.value))
    print('d = {}'.format(d.value))
    print('e = {}'.format(e.value))

