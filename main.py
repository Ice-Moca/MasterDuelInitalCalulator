import function
from typing import List, Dict, Set

if __name__ == "__main__":
    print("Calculating conflict probabilities...")

    # 입력 데이터 정의
    total_cards = [
        {'name': '우라라', 'count': 3},
        {'name': '증쥐', 'count': 3},
        {'name': '마술사1', 'count': 3},
        {'name': '마술사2', 'count': 3},
        {'name': '마술사3', 'count': 2},
        {'name': '마법1', 'count': 3},
        {'name': '마법2', 'count': 3},
        {'name': '마법3', 'count': 3},
        {'name': '아스트로', 'count': 3},
        {'name': '말림패1', 'count': 2}
    ]
    desired_cards = ['마술사1', '마술사2', '마술사3', '마법1', '마법2', '마법3', '아스트로']
    draw_count = True  # True for going first, False for going second
    hands = [1, 2, 3]
    hand_sets = [{'마법1'},{'마법2'},{'마법3'}, {'마술사1', '마술사2'},{'마술사1', '마술사3'},{ '마술사2', '마술사3', '아스트로'}]
    crash = ['말림패1']
    hand = 1  # 단일 hand_prob 테스트용

    # 필요한 변수 세팅
    base_draw = 5 if draw_count else 6
    deck_dict = {card['name']: card['count'] for card in total_cards}

    # 확률 계산
    total_prob = function.calculate_probability(total_cards, desired_cards, draw_count, hands, hand_sets, crash, prob_out_crash=True)
    print("전체 확률 목록:", total_prob)

    hand_prob = function.calculate_hand_probability(deck_dict, desired_cards, base_draw, hand, hand_sets)
    print(f"{hand}핸드 확률:", hand_prob)

    conflict_prob = function.calculate_conflict_probability(deck_dict, crash, base_draw)
    print("충돌 확률:", conflict_prob)

    union_prob = function.calculate_union_hand_probability(deck_dict, base_draw, hand_sets, crash, prob_out_crash=True)
    print("합집합 확률:", union_prob)


# 1. 말림패를 뺄거냐? (근사정도) 
# 2. 패트랩을 잡을 확률을 넣을 거냐? (쉽긴함)

# 3. 애매한 1.5핸드 같은거 처리를 어떻게 할거냐? 하얀숲 
# + 애매한 초동 카드들

# 4. 증쥐를 막을 패트랩 잡을 확률 
# 지명자 말명자 우라라 드롤 