# TODO:
# - 성능 개션한 다른 버전 함수 추가
# - 파이썬스러운 단위 테스트 코드로 변경

def count_number_of_prime_numbers_up_to(n: int) -> int:
    count = 0
    for i in range(2, n + 1):
        for j in range(2, i):
            if i % j == 0:
                break
        else:
            count += 1
    return count
