"""
負責建立資料表，並將占卜結果寫入 history.db
"""
import json
import sqlite3
from datetime import datetime
import os

class HistoryManager:
    def __init__(self, db_path):
        self.db_path = db_path
        # 確保資料夾存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 💡 確保這裡的欄位名稱是 cards_json
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    spread_type TEXT,
                    cards_json TEXT
                )
            ''')
            conn.commit()

    def save_record(self, spread_type, cards_data):
        """將卡片資料轉為 JSON 字串並儲存"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 💡 將 list/dict 轉為 JSON 字串
                cards_json = json.dumps(cards_data, ensure_ascii=False)
                
                cursor.execute(
                    "INSERT INTO history (timestamp, spread_type, cards_json) VALUES (?, ?, ?)",
                    (timestamp, spread_type, cards_json)
                )
                conn.commit()
        except Exception as e:
            print(f"❌ 儲存失敗: {e}")

    def clear_all(self):
        """
        刪除資料庫中所有的占卜紀錄
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM history")
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ 刪除紀錄時發生錯誤: {e}")
            return False
    
    def get_recent_history(self, limit=5):
        """取得最近的占卜紀錄"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 讓回傳結果變成字典格式，方便讀取
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, timestamp, spread_type, cards_json FROM history ORDER BY timestamp DESC LIMIT ?", 
                    (limit,)
                )
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ 讀取資料失敗: {e}")
            return []