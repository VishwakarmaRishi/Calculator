import math

fact = math.factorial
rad = math.radians


def log(number):
    return round(math.log10(number), 3)


def ln(number):
    return round(math.log(number), 3)


def sin(angle, unit=rad):
    return round(math.sin(unit(angle)), 3)


def cos(angle, unit=rad):
    return round(math.cos(unit(angle)), 3)


def tan(angle, unit=rad):
    return round(math.tan(unit(angle)), 3)


def csc(angle, unit=rad):
    return round(1 / sin(angle), 3)


def sec(angle, unit=rad):
    return round(1 / cos(angle), 3)


def cot(angle, unit=rad):
    return round(1 / tan(angle), 3)


def HCF_of_2(x, y):
    while y:
        x, y = y, x % y
    return x


def HCF(*numbers):
    if len(numbers) == 2:
        return HCF_of_2(*numbers)
    else:
        numbers = list(numbers)
        for i in range(len(numbers) - 1):
            numbers.append(HCF_of_2(numbers.pop(), numbers.pop()))
        return numbers[0]


def LCM_of_2(x, y):
    return x * y // HCF(x, y)


def LCM(*numbers):
    if len(numbers) == 2:
        return LCM_of_2(*numbers)
    else:
        numbers = list(numbers)
        for i in range(len(numbers) - 1):
            numbers.append(LCM_of_2(numbers.pop(), numbers.pop()))
        return numbers[0]


__all__ = [fact, rad, log, ln, sin, cos, tan, csc, sec, cot, HCF, LCM]
