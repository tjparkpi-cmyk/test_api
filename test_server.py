import os
import json
import time
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 1. 초기 변수값 설정
state = {
    "message": "엔트리 서버 연동 성공!",
    "count": 0
}

# 2. 1초마다 변수값을 바꾸고 data.json으로 자동 저장하는 함수
def update_json_loop():
    while True:
        state["count"] += 1
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            
        print(f"data.json 업데이트됨 -> count: {state['count']}")
        time.sleep(1)

# 3. 엔트리 접속(CORS)을 허용하는 서버 설정
class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        pass

# 백그라운드 자동화 시작
threading.Thread(target=update_json_loop, daemon=True).start()

# 4. 로컬(8000)과 클라우드(PORT 환경변수) 모두 지원하는 서버 실행부
port = int(os.environ.get("PORT", 8000))
print(f"서버 시작됨 (포트: {port})")
HTTPServer(('0.0.0.0', port), CORSRequestHandler).serve_forever()
