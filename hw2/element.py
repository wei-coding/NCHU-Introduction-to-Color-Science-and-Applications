def main():
    '''
    get input
    '''
    (n, k, m) = input().strip().split(' ')
    (n, k, m) = (int(n), int(k), int(m))
    print(element(n, k, m))


def cobidic(n, k, m) -> list:
    '''
    Fool-proofing
    '''
    if (n > 81 or n < 1):
        raise ValueError('Error input in n: 1 <= n <= 81')
    if (k > n or k < 1):
        raise ValueError('Error input in k: 1 <= k <= n')
    if (m >= C(n, k) or m < 0):
        raise ValueError('Error input in m: must less than C(n,k)')
    '''
    Algorithm itself
    '''
    ki = k
    cobidic_list = []
    while m >= 0 and ki > 0:
        for i in range(1, n + 1):
            c_now = C(n - i, ki)
            if c_now <= m:
                cobidic_list.append(n - i)
                m -= c_now
                break
        ki -= 1
        n -= 1
    return cobidic_list


def element(n, k, m) -> list:
    d = C(n, k) - 1 - m
    cobidic_d = cobidic(n, k, d)
    element_list = [n - 1 - x for x in cobidic_d]
    return element_list


def C(n, k) -> int:
    if (n >= k):
        try:
            return factorial(n) // factorial(k) // factorial(n - k)
        except ValueError:
            print(f'(n ,k) = ({n}, {k})\nfactorial() not defined for negative values')
    else:
        return 0


def factorial(n) -> int:
    t = 1
    for i in range(1, n + 1):
        t *= i
    return t


if __name__ == '__main__':
    main()
