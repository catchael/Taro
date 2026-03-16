"""
讀取 JSON 並進行「抽牌」：洗牌、抽牌邏輯
"""

import json
import random
import os

class Deck:
    def __init__(self, data_path="data/cards.json"):
        with open(data_path, "r", encoding="utf-8") as f:
            self.cards = json.load(f)

    def draw(self, count=1):
        # 隨機抽取卡牌，不重複
        keys = random.sample(list(self.cards.keys()), count)
        results = []
        for k in keys:
            card = self.cards[k].copy()
            card["is_reversed"] = random.choice([True, False])
            results.append(card)
        return results