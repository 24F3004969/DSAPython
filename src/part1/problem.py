def main():
    print(read_lines_and_solve(0, 0, 0, ""), end='')


def read_lines_and_solve(i, n, max_term, final_result):
    if i <= n:
        line = input()
    if i > n and i != 0:
        return final_result
    if n == 0:
        n = int(line) * 2
    elif i % 2 != 0:
        max_term = int(line)
    elif i % 2 == 0 and i != 0:
        if i < n:
            final_result += str(get_sum_of_spaced_number(line + " ", 0, 0, max_term, 0)) + '\n'
        else:
            final_result += str(get_sum_of_spaced_number(line + " ", 0, 0, max_term, 0))

    return read_lines_and_solve(i + 1, n, max_term, final_result)


def look_for_char_before_space(s, i, result):
    if i == len(s) or s[i] == ' ':
        return result, i
    else:
        return look_for_char_before_space(s, i + 1, result + s[i])


def get_sum_of_spaced_number(x, su, ind, no_terms, i):
    re, ind = look_for_char_before_space(x, ind, "")
    if ind >= len(x):
        if i < no_terms:
            return -1
        return su
    else:
        if int(re) < 0:
            return get_sum_of_spaced_number(x, int(su) + int(re) ** 4, ind + 1, no_terms, i + 1)
        else:
            return get_sum_of_spaced_number(x, int(su), ind + 1, no_terms, i + 1)


if __name__ == '__main__':
    main()
