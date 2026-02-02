import os
from flask import Flask, render_template_string, request
import google.genai as genai
import datetime
import random
import ephem
import pytz
from lunar_python import Lunar, Solar
import markdown

# Flask 앱 설정
app = Flask(__name__)

# API 키 가져오기 (Secrets 연동 필수)
MY_API_KEY = os.environ.get("GOOGLE_API_KEY")

# ==========================================
# [로직 1] 주역 64괘 (100% Full Data)
# ==========================================
def get_real_iching():
    hexagrams = [
        "1. 중천건(乾) - 위대한 하늘, 강건함, 창조적 에너지", "2. 중지곤(坤) - 포용하는 땅, 유순함, 어머니의 품",
        "3. 수뢰둔(屯) - 험난한 시작, 인내하며 싹을 틔움", "4. 산수몽(蒙) - 어리석음을 깨우침, 배움의 시기",
        "5. 수천수(需) - 때를 기다림, 인내와 준비", "6. 천수송(訟) - 다툼과 소송, 물러서서 타협해야 함",
        "7. 지수사(師) - 군대를 이끄는 리더십, 엄격한 규율", "8. 수지비(比) - 사람들과 친밀하게 어울림, 협력",
        "9. 풍천소축(小畜) - 잠시 멈춤, 구름은 끼었으나 비는 아직 안 옴", "10. 천택리(履) - 호랑이 꼬리를 밟음, 예의와 조심성",
        "11. 지천태(泰) - 태평성대, 하늘과 땅의 화합 (길)", "12. 천지비(否) - 막혀있는 운세, 소통이 필요함",
        "13. 천화동인(同人) - 뜻을 같이하는 동료, 협동", "14. 화천대유(大有) - 크게 가짐, 태양이 하늘에 뜸 (대길)",
        "15. 지산겸(謙) - 겸손하면 형통함, 자신을 낮춤", "16. 뇌지예(豫) - 미리 준비하고 즐거워함",
        "17. 택뢰수(隨) - 흐름을 따름, 임기응변", "18. 산풍고(蠱) - 부패를 척결하고 새롭게 함",
        "19. 지택림(臨) - 군자가 다가옴, 성대한 기운", "20. 풍지관(觀) - 냉철한 관찰, 본보기가 됨",
        "21. 화뢰서합(噬嗑) - 방해물을 씹어 없앰, 법 집행", "22. 산화비(賁) - 아름답게 꾸밈, 외면의 화려함",
        "23. 산지박(剝) - 깎여나감, 쇠퇴기, 기초를 다져야 함", "24. 지뢰복(復) - 다시 돌아옴, 회복의 기운",
        "25. 천뢰무망(無妄) - 거짓 없이 진실함, 자연스러움", "26. 산천대축(大畜) - 크게 쌓음, 인재를 기름",
        "27. 산뢰이(頤) - 올바른 양육, 말조심과 음식 조절", "28. 택풍대과(大過) - 기둥이 휨, 과도한 부담",
        "29. 중수감(坎) - 첩첩산중, 험난한 물, 지혜로 극복", "30. 중화리(離) - 타오르는 불, 지혜와 문명, 이별",
        "31. 택산함(咸) - 마음이 통함, 감동과 사랑", "32. 뇌풍항(恒) - 변함없이 꾸준함, 지속성",
        "33. 천산둔(遯) - 물러나서 은둔함, 때를 기다리는 지혜", "34. 뇌천대장(大壯) - 용맹하고 씩씩함, 폭주 주의",
        "35. 화지진(晉) - 나아가 승진함, 밝은 해가 떠오름", "36. 지화명이(明夷) - 빛이 땅에 가려짐, 고난 속의 지혜",
        "37. 풍화가인(家人) - 가정의 화목, 본분에 충실", "38. 화택규(睽) - 서로 어긋나고 반목함, 다름을 인정",
        "39. 수산건(蹇) - 가다가 멈춤, 어려움에 직면", "40. 뇌수해(解) - 어려움이 풀림, 해결의 실마리",
        "41. 산택손(損) - 덜어냄, 봉사와 희생 후의 이익", "42. 풍뢰익(益) - 더함, 바람과 우뢰가 도움 (길)",
        "43. 택천쾌(夬) - 결단하여 제거함, 과감한 결정", "44. 천풍구(姤) - 우연한 만남, 유혹을 조심",
        "45. 택지췌(萃) - 사람들이 모여듦, 번창과 축제", "46. 지풍승(升) - 땅 속에서 나무가 자람, 상승운",
        "47. 택수곤(困) - 곤란함, 물이 말라버린 연못", "48. 수풍정(井) - 마르지 않는 우물, 변치 않는 덕",
        "49. 택화혁(革) - 옛것을 버리고 새롭게 고침, 혁신", "50. 화풍정(鼎) - 솥에 음식을 끓임, 안정과 쇄신",
        "51. 중뢰진(震) - 우르릉 쾅쾅, 놀라지만 깨달음이 있음", "52. 중산간(艮) - 산처럼 멈춰 서서 안정을 찾음",
        "53. 풍산점(漸) - 차근차근 나아감, 순서대로 진행", "54. 뇌택귀매(歸妹) - 순서가 뒤바뀜, 불안정한 관계",
        "55. 뇌화풍(豐) - 풍요롭고 성대함, 전성기", "56. 화산여행(旅) - 나그네의 여행, 불안정하지만 자유로움",
        "57. 중풍손(巽) - 공손하게 스며듦, 바람 같은 유연함", "58. 중택태(兌) - 기쁨과 즐거움, 연못과 소녀",
        "59. 풍수환(渙) - 흩어짐, 근심 해소, 멀리 나아감", "60. 수택절(節) - 대나무 마디, 절제와 규칙",
        "61. 풍택중부(中孚) - 마음속의 진실, 믿음", "62. 뇌산소과(小過) - 작은 새가 나는 형상, 겸손해야 함",
        "63. 수화기제(旣濟) - 이미 건너감, 완성, 성취", "64. 화수미제(未濟) - 아직 건너지 못함, 미완성, 새로운 시작"
    ]
    return random.choice(hexagrams)

# ==========================================
# [로직 2] 타로 78장 (100% Full Data)
# ==========================================
def get_real_tarot():
    major = [
        "0. The Fool (바보)", "I. The Magician (마법사)", "II. The High Priestess (여사제)",
        "III. The Empress (여황제)", "IV. The Emperor (황제)", "V. The Hierophant (교황)",
        "VI. The Lovers (연인)", "VII. The Chariot (전차)", "VIII. Strength (힘)",
        "IX. The Hermit (은둔자)", "X. Wheel of Fortune (운명의 수레바퀴)", "XI. Justice (정의)",
        "XII. The Hanged Man (매달린 남자)", "XIII. Death (죽음)", "XIV. Temperance (절제)",
        "XV. The Devil (악마)", "XVI. The Tower (탑)", "XVII. The Star (별)",
        "XVIII. The Moon (달)", "XIX. The Sun (태양)", "XX. Judgement (심판)", "XXI. The World (세계)"
    ]
    suits = {"Wands": "행동/열정", "Cups": "감정/사랑", "Swords": "이성/고난", "Pentacles": "물질/현실"}
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
    
    minor = []
    for suit_name, keyword in suits.items():
        for rank in ranks:
            minor.append(f"{rank} of {suit_name} ({keyword})")
            
    full_deck = major + minor
    return random.choice(full_deck)

# ==========================================
# [로직 3] 점성술, 기문둔갑, 수비학, 사주
# ==========================================
def get_real_astrology(year, month, day, hour, minute):
    try:
        obs = ephem.Observer()
        obs.lat, obs.lon = '37.5665', '126.9780' # Seoul
        obs.date = datetime.datetime(year, month, day, hour, minute) - datetime.timedelta(hours=9)
        sun = ephem.Sun(obs); sun.compute(obs); moon = ephem.Moon(obs); moon.compute(obs)
        return f"태양[{ephem.constellation(sun)[1]}], 달[{ephem.constellation(moon)[1]}]"
    except: return "천문 정보 계산 불가"

def get_real_qimen(year, month, day, hour):
    try:
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        wealth_pos = lunar.getDayPositionCai()
        d_map = {"震":"동쪽(E)","兌":"서쪽(W)","離":"남쪽(S)","坎":"북쪽(N)","巽":"남동쪽(SE)","坤":"남서쪽(SW)","乾":"북서쪽(NW)","艮":"북동쪽(NE)"}
        return f"{d_map.get(wealth_pos, wealth_pos)}"
    except: return "방위 정보 계산 불가"

def get_numerology_data(year, month, day):
    # 1. 운명수 (Life Path)
    total = sum(int(d) for d in str(year)) + sum(int(d) for d in str(month)) + sum(int(d) for d in str(day))
    life_path = total
    while life_path > 9:
        if life_path in [11, 22, 33]: break
        life_path = sum(int(d) for d in str(life_path))
    
    # 2. 일운수 (Personal Day)
    now = datetime.datetime.now()
    p_total = sum(int(d) for d in str(now.year)) + sum(int(d) for d in str(month)) + sum(int(d) for d in str(day))
    personal_day = p_total
    while personal_day > 9:
        personal_day = sum(int(d) for d in str(personal_day))
        
    return str(life_path), str(personal_day)

def get_numerology_meaning(number):
    meanings = {
        "1": "개척과 독립", "2": "조화와 협력", "3": "창조와 표현", "4": "안정과 질서", 
        "5": "변화와 자유", "6": "책임과 봉사", "7": "분석과 통찰", "8": "성취와 권력", 
        "9": "완성과 포용", "11": "영적 직관(Master)", "22": "위대한 실행(Master)", "33": "헌신적 사랑(Master)"
    }
    return meanings.get(str(number), "")

def get_saju(year, month, day, hour, minute):
    try:
        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        bazi = solar.getLunar().getBaZi()
        return f"일간: {bazi[2]}"
    except: return "사주 정보 없음"

# ---------------------------------------------------------
# [라우팅] 웹페이지 동작
# ---------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    ai_result = ""
    user_data = ""
    
    if request.method == "POST":
        try:
            name = request.form.get("name")
            b_date = request.form.get("birth_date") # YYYYMMDD
            b_time = request.form.get("birth_time") # HH:MM
            
            # 날짜 처리
            dt = datetime.datetime.strptime(f"{b_date} {b_time}", "%Y%m%d %H:%M")
            
            # 1. 6대 운세 로직 실행
            saju = get_saju(dt.year, dt.month, dt.day, dt.hour, dt.minute)
            life_path, personal_day = get_numerology_data(dt.year, dt.month, dt.day)
            iching = get_real_iching()
            tarot = get_real_tarot()
            astro = get_real_astrology(dt.year, dt.month, dt.day, dt.hour, dt.minute)
            qimen = get_real_qimen(dt.year, dt.month, dt.day, dt.hour)
            
            user_data = f"""
            <div class='data-box'>
                <p><strong>{name}님의 운명 코드</strong></p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9em;">
                    <div>🀄 {saju}</div>
                    <div>🔢 운명수 {life_path} ({get_numerology_meaning(life_path)})</div>
                    <div>📅 오늘 {personal_day} ({get_numerology_meaning(personal_day)})</div>
                    <div>🧭 길방: {qimen}</div>
                    <div>🪐 {astro}</div>
                    <div>☯️ {iching.split('-')[0]}</div>
                    <div>🃏 {tarot}</div>
                </div>
            </div>
            """
            
            # 2. Gemini AI 호출 (프리미엄 프롬프트)
            if MY_API_KEY:
                client = genai.Client(api_key=MY_API_KEY)
                prompt = f"""
                저는 대한민국 최고의 운세 전략가입니다. {name}님의 데이터를 바탕으로 오늘 하루 실전 가이드를 작성해드립니다.
                
                [분석 데이터]
                - 🀄 사주: {saju}
                - 🔢 수비학: 운명수 {life_path}, 오늘의 일운수 {personal_day}
                - 🧭 기문둔갑: {qimen}
                - 🪐 점성술: {astro}
                - ☯️ 주역: {iching}
                - 🃏 타로: {tarot}

                [작성 필수 가이드]
                - 제목 반복 금지. 바로 본문 시작.
                - 점수와 한 줄 요약 사이에는 반드시 한 줄 띄울 것.
                - 구체적인 행동 강령 포함 (해야 할 일, 피해야 할 일, 행운 아이템)
                - 말투는 명확하고 세련되게 (잡지 에디터처럼)

                ---
                ## 🎯 DAILY SUMMARY
                **점수:** ___/100
                
                **KEYWORD:** (오늘을 관통하는 핵심 단어)
                
                (전체적인 운세 흐름 요약...)
                
                ## 📋 ACTION PLAN
                ### ✅ TO DO (3가지)
                1. **(시간/장소):** (행동)
                   - 이유:
                2. ...
                3. ...

                ### ❌ NOT TO DO (3가지)
                1. 
                2. 
                3. 

                ### 🍀 LUCKY ITEMS
                - **COLOR:**
                - **NUMBER:**
                - **FOOD:**
                - **DIRECTION:** {qimen}
                """
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                ai_result = markdown.markdown(response.text)
            else:
                ai_result = "<p style='color:red;'>⚠️ API 키가 설정되지 않았습니다. Secrets를 확인하세요.</p>"
                
        except Exception as e:
            ai_result = f"<p style='color:red;'>입력 형식을 확인해주세요. (예: 19900101, 14:30) / 에러: {e}</p>"

    # HTML 템플릿 (Freshman Style + Texture)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Destiny Strategist</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&display=swap');
            
            body {{ 
                background-color: #B2B2A8; 
                background-image: url("https://www.transparenttextures.com/patterns/noise-lines.png");
                color: #111; 
                font-family: 'DM Sans', sans-serif; 
                padding: 20px; 
                line-height: 1.6; 
            }}
            
            .container {{ max-width: 800px; margin: 0 auto; }}
            
            h1 {{ 
                font-family: 'Playfair Display', serif; 
                font-size: 3.5rem; 
                text-transform: uppercase; 
                border-bottom: 3px solid #111; 
                padding-bottom: 10px; 
                margin-bottom: 40px; 
                line-height: 1.0;
            }}
            
            input, button {{ 
                width: 100%; 
                padding: 15px; 
                margin-bottom: 10px; 
                border: 2px solid #111; 
                background: rgba(255,255,255,0.3); 
                font-family: 'DM Sans', sans-serif; 
                font-size: 16px; 
                box-sizing: border-box; 
                font-weight: bold;
                color: #111;
            }}
            
            /* 입력창 플레이스홀더 색상 조정 */
            ::placeholder {{ color: #555; opacity: 1; }}
            
            button {{ 
                background: #111; 
                color: #B2B2A8; 
                cursor: pointer; 
                text-transform: uppercase; 
                transition: 0.3s; 
                margin-top: 10px;
            }}
            button:hover {{ background: transparent; color: #111; }}
            
            .data-box {{ 
                border: 1px dashed #111; 
                padding: 20px; 
                margin-bottom: 30px; 
                background: rgba(255,255,255,0.1); 
                font-size: 14px;
            }}
            
            .report-box {{ 
                border: 3px solid #111; 
                padding: 30px; 
                background: rgba(255,255,255,0.4); 
                backdrop-filter: blur(5px);
            }}
            
            h2, h3 {{ 
                font-family: 'Playfair Display', serif; 
                margin-top: 30px; 
                border-top: 1px solid #555; 
                padding-top: 10px; 
            }}
            
            strong {{ color: #a33; }}
            
            /* 모바일 대응 */
            @media (max-width: 600px) {{
                h1 {{ font-size: 2.5rem; }}
                .report-box {{ padding: 15px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Destiny<br>Strategist</h1>
            <p>당신을 위한 6차원 심층 분석 리포트</p>
            <br>
            
            <form method="POST">
                <input type="text" name="name" placeholder="YOUR NAME (이름)" required>
                <input type="text" name="birth_date" placeholder="BIRTH DATE (ex: 19900101)" required>
                <input type="text" name="birth_time" placeholder="BIRTH TIME (ex: 14:30)" required>
                <button type="submit">ANALYZE DESTINY</button>
            </form>
            
            {user_data}
            
            {'<div class="report-box">' + ai_result + '</div>' if ai_result else ''}
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)