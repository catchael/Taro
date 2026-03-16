import google.generativeai as genai
import os

class TarotAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

    def analyze_spread(self, question: str, spread_results: list):
        """
        將牌陣結果傳給 AI 進行深度解析
        """
        # 組合牌面資訊
        card_info = ""
        for pos, card in spread_results:
            status = "逆位" if card['is_reversed'] else "正位"
            card_info += f"- 位置: {pos}, 牌名: {card['name']}, 狀態: {status}\n"

        # 撰寫 Prompt
        prompt = f"""
        你是一位專業且充滿智慧的塔羅占卜師。
        使用者的問題是：「{question}」
        
        本次抽出的牌陣如下：
        {card_info}
        
        請根據各個位置的含義與牌義，為使用者提供一段溫暖、具啟發性且深入的解析。
        解析要求：
        1. 語氣要專業且神祕。
        2. 針對「過去、現在、未來」的關聯性進行邏輯串連。
        3. 最後給予一個具體的行動建議。
        **請使用繁體中文回答。**
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ AI 占卜暫時斷線了... 錯誤原因: {str(e)}"