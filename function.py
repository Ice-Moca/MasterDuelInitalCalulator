from math import comb, floor
from typing import List, Dict, Tuple, Set
from itertools import combinations

def is_all_integer_floats(hands: List[float]) -> bool:
    try:
        return all(float(x).is_integer() for x in hands)
    except ValueError:
        return False

def generate_n_union_sets(hand_sets: List[Set[str]], comb_num: int, max_size: int = 5) -> List[Set[str]]:
    # N개의 핸드 세트에서 조합 생성
    # 5장을 넘어가는 조합은 제외
    seen = set()
    result = []
    
    # 각 핸드에서 가능한 모든 조합을 생성
    # {A,B},{B,C} -> {A,B,C} 형태로 union
    for combo in combinations(hand_sets, comb_num):
        union = set().union(*combo)
        if len(union) <= max_size:
            frozen = frozenset(union)
            if frozen not in seen:
                seen.add(frozen)
                result.append(union)
    # 이후 코드에서 포함 배제로 확률 계산할 것
    print(result)
    return result

def calculate_conflict_probability(deck_dict: Dict[str, int], crash: List[str], base_draw: int) -> float:
    # 기본 변수 설정
    deck_size = sum(deck_dict.values())
    length = len(crash)
    conflict_prob = 0.0

    # Valid input 확인
    if any(card not in deck_dict for card in crash):
        print(f"Conflict set {crash} contains cards not in deck.")
        return 0.0

    # 각 카드 조합에 대해 확률 계산
    for i in range(1, length + 1):
        for card_set in combinations(crash, i):
            card_num = sum(deck_dict[card] for card in card_set)
            prob = 1 - comb(deck_size - card_num, base_draw) / comb(deck_size, base_draw)
            conflict_prob += prob if i % 2 == 1 else -prob

    return conflict_prob

def calculate_hand_probability(deck_dict: Dict[str, int], desired_cards: List[str], base_draw: int, hand: int, hand_sets: List[Set[str]]) -> float:
    # 핸드에 맞는 카드 세트 필터링
    filtered_sets = [s for s in hand_sets if len(s) == hand]
    
    # Valid input 확인
    if any(card not in desired_cards for s in filtered_sets for card in s):
        print(f"Filtered hand sets contain cards not in desired cards.")
        return 0.0

    # 필터링된 세트가 비어있으면 확률 0 반환
    if not filtered_sets:
        print("No valid hand sets found.")
        return 0.0

    # 기본 변수 설정
    depth = len(filtered_sets)
    hand_prob = 0.0
    deck_size = sum(deck_dict.values())

    # 각 카드 조합에 대해 확률 계산
    for i in range(1, depth + 1):
        unions = generate_n_union_sets(filtered_sets, i)
        for u_set in unions:
            prob = probability_of_inclusion(deck_dict, base_draw, u_set)
            hand_prob += prob if i % 2 == 1 else -prob
            
    return hand_prob

def probability_of_inclusion(deck_dict: Dict[str, int], base_draw: int, card_set: Set[str]) -> float:
    deck_size = sum(deck_dict.values())
    prob = 0.0
    cards = list(card_set)
    n = len(cards)

    for i in range(1, n + 1):
        for sub_cards in combinations(cards, i):
            card_num = sum(deck_dict.get(card, 0) for card in sub_cards)
            p = 1 - comb(deck_size - card_num, base_draw) / comb(deck_size, base_draw)
            prob += p if i % 2 == 1 else -p

    return prob

def calculate_probability(
    total_cards: List[Dict[str, int]],
    desired_cards: List[str],
    draw_count: bool,
    hands: List[float],
    hand_sets: List[Set[str]],
    crash: List[str],
    prob_out_crash: bool = False
) -> List[float]:
    
    # Valid input 확인
    if max(hands) > 5 or min(hands) < 1:
        print("Invalid number of hands. Must be between 1 and 5.")
        return []

    # 입력된 핸드가 정수인지 확인
    if not is_all_integer_floats(hands):
        print("Invalid number of hands. Must be integer floats.")
        return []

    # 기본 변수 설정
    base_draw = 5 if draw_count else 6
    deck_dict = {card['name']: card['count'] for card in total_cards}
    prob_list = []

    # 각 핸드에 대해 확률 계산
    for hand in hands:
        h = floor(hand)
        prob = calculate_hand_probability(deck_dict, desired_cards, base_draw, h, hand_sets)

        if prob_out_crash:
            crash_prob = calculate_conflict_probability(deck_dict, crash, base_draw)
            prob *= (1 - crash_prob)

        prob_list.append(prob)

    return prob_list

def calculate_union_hand_probability(deck_dict: Dict[str, int], base_draw: int, hand_sets: List[Set[str]], crash: List[str], prob_out_crash: bool=True) -> float:
    """
    여러 hand_sets가 주어졌을 때, 이들 각각의 합집합 확률을 포함 배제 원리에 따라 계산
    """
    depth = len(hand_sets)
    if depth == 0:
        return 0.0

    total_prob = 0.0

    for i in range(1, depth + 1):
        for union_set in generate_n_union_sets(hand_sets, i):
            prob = probability_of_inclusion(deck_dict, base_draw, union_set)
            total_prob += prob if i % 2 == 1 else -prob

    if prob_out_crash:
        crash_prob = calculate_conflict_probability(deck_dict, crash, base_draw)
        total_prob *= (1 - crash_prob)
    
    return total_prob
