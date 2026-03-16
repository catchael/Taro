"""
牌陣定義 (三牌陣、凱爾特十字等)
"""
class SpreadEngine:
    def __init__(self, deck):
        self.deck = deck

    def three_cards(self):
        """過去、現在、未來"""
        cards = self.deck.draw(3)
        positions = ["過去", "現在", "未來"]
        return list(zip(positions, cards))

    def daily_one(self):
        """每日指引"""
        cards = self.deck.draw(1)
        return [("今日指引", cards[0])]