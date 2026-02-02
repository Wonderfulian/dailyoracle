<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 주역 점치기 (Premium)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;500;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
    <style>
        body {
            font-family: 'Noto Serif KR', serif;
            background-color: #f4f1ea;
            color: #3e3a36;
        }
        .yin-line {
            display: flex;
            justify-content: space-between;
            width: 100%;
            height: 24px;
            margin: 6px 0;
        }
        .yin-part {
            width: 42%;
            background-color: #2c2c2c;
            border-radius: 2px;
        }
        .yang-line {
            width: 100%;
            height: 24px;
            background-color: #2c2c2c;
            margin: 6px 0;
            border-radius: 2px;
        }
        .loader {
            border: 3px solid #f3f3f3;
            border-radius: 50%;
            border-top: 3px solid #5d4037;
            width: 24px;
            height: 24px;
            -webkit-animation: spin 1s linear infinite; /* Safari */
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        /* Markdown Prose Styling for Report */
        .markdown-prose h2 {
            font-size: 1.5em;
            font-weight: 700;
            margin-top: 1.5em;
            margin-bottom: 0.8em;
            color: #2c2c2c;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 0.3em;
        }
        .markdown-prose h3 {
            font-size: 1.2em;
            font-weight: 700;
            margin-top: 1.2em;
            margin-bottom: 0.5em;
            color: #4a4a4a;
        }
        .markdown-prose p {
            margin-bottom: 1em;
            line-height: 1.8;
            word-break: keep-all;
        }
        .markdown-prose ul {
            list-style-type: none;
            padding-left: 0;
            margin-bottom: 1em;
        }
        .markdown-prose li {
            position: relative;
            padding-left: 1.2em;
            margin-bottom: 0.5em;
        }
        .markdown-prose li:before {
            content: "•";
            position: absolute;
            left: 0;
            color: #8d6e63;
        }
        .markdown-prose strong {
            color: #5d4037;
            font-weight: 700;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center p-4">

    <!-- Main Container -->
    <div class="bg-white w-full max-w-3xl rounded-xl shadow-2xl overflow-hidden border border-stone-200">
        
        <!-- Header -->
        <div class="bg-stone-800 text-stone-100 p-8 text-center relative">
            <h1 class="text-3xl font-bold mb-2">AI 주역 점치기 <span class="text-yellow-500 text-lg align-top">Premium</span></h1>
            <p class="text-stone-300 text-sm opacity-80">사주, 수비학, 타로, 주역이 결합된 종합 운세 리포트</p>
        </div>

        <!-- Input Section -->
        <div class="p-6 md:p-8 space-y-6">
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm font-bold text-stone-600 mb-1">이름</label>
                    <input type="text" id="userName" placeholder="예: 홍길동"
                        class="w-full bg-stone-50 border border-stone-300 rounded px-3 py-2 focus:outline-none focus:border-stone-500 focus:ring-1 focus:ring-stone-500 transition-colors">
                </div>
                <div>
                    <label class="block text-sm font-bold text-stone-600 mb-1">생년월일 (YYYYMMDD)</label>
                    <input type="text" id="birthDate" placeholder="예: 19900101" maxlength="8"
                        class="w-full bg-stone-50 border border-stone-300 rounded px-3 py-2 focus:outline-none focus:border-stone-500 focus:ring-1 focus:ring-stone-500 transition-colors">
                </div>
                <div>
                    <label class="block text-sm font-bold text-stone-600 mb-1">태어난 시간 (HH:MM)</label>
                    <input type="time" id="birthTime"
                        class="w-full bg-stone-50 border border-stone-300 rounded px-3 py-2 focus:outline-none focus:border-stone-500 focus:ring-1 focus:ring-stone-500 transition-colors">
                </div>
            </div>

            <!-- Question/Intent (Optional) -->
            <div>
                <label class="block text-sm font-bold text-stone-600 mb-1">고민이나 궁금한 점 (선택)</label>
                <input type="text" id="query" placeholder="예: 이번 달 사업 확장이 괜찮을까요? 연애운이 궁금합니다."
                    class="w-full bg-stone-50 border border-stone-300 rounded px-3 py-2 focus:outline-none focus:border-stone-500 focus:ring-1 focus:ring-stone-500 transition-colors">
            </div>

            <!-- Action Button -->
            <button onclick="drawFortune()" id="drawBtn"
                class="w-full bg-stone-700 hover:bg-stone-800 text-white font-bold py-4 rounded-lg shadow-lg transition-all transform active:scale-[0.99] flex items-center justify-center gap-2 text-lg">
                <i class="fas fa-yin-yang"></i> 프리미엄 운세 리포트 생성
            </button>

            <!-- Error Message Area -->
            <div id="errorMessage" class="hidden bg-red-50 text-red-700 p-3 rounded text-sm border border-red-200"></div>
        </div>

        <!-- Result Section -->
        <div id="resultSection" class="hidden bg-stone-50 border-t border-stone-200">
            
            <div class="p-6 md:p-8">
                <!-- Data Summary Cards -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                     <div class="bg-white p-3 rounded border border-stone-200 text-center">
                        <div class="text-xs text-stone-500 uppercase tracking-wider mb-1">수비학 (운명수)</div>
                        <div class="font-bold text-stone-800" id="dispLifePath">-</div>
                     </div>
                     <div class="bg-white p-3 rounded border border-stone-200 text-center">
                        <div class="text-xs text-stone-500 uppercase tracking-wider mb-1">타로 카드</div>
                        <div class="font-bold text-stone-800 text-sm" id="dispTarot">-</div>
                     </div>
                     <div class="bg-white p-3 rounded border border-stone-200 text-center col-span-2 md:col-span-2 flex flex-col items-center justify-center">
                        <div class="text-xs text-stone-500 uppercase tracking-wider mb-1">주역 (Hexagram)</div>
                        <div id="hexagramVisual" class="w-full h-8 flex flex-col justify-between items-center opacity-80"></div>
                     </div>
                </div>

                <!-- Interpretation -->
                <div class="border-t border-stone-200 pt-6">
                    <h3 class="text-lg font-bold text-stone-800 mb-3 flex items-center gap-2">
                        <i class="fas fa-file-alt text-stone-500"></i> 실전 가이드 리포트
                    </h3>
                    
                    <div id="loading" class="hidden flex flex-col items-center justify-center py-12 text-stone-500">
                        <div class="loader mb-4"></div>
                        <p id="loadingText" class="text-lg font-medium">운명 데이터를 분석 중입니다...</p>
                        <p class="text-sm text-stone-400 mt-2">사주, 수비학, 기문둔갑, 주역 통합 분석 중 (약 15초 소요)</p>
                    </div>

                    <div id="interpretation" class="markdown-prose text-stone-700 text-sm md:text-base hidden bg-white p-6 rounded-lg shadow-sm border border-stone-100">
                        <!-- AI Content will go here -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const apiKey = ""; // API key is injected by the environment

        // --- Logic: Numerology ---
        function calculateLifePathNumber(birthDateStr) {
            // birthDateStr format: YYYYMMDD
            let sum = 0;
            for (let char of birthDateStr) {
                sum += parseInt(char, 10);
            }
            while (sum > 9 && sum !== 11 && sum !== 22 && sum !== 33) {
                let tempSum = 0;
                String(sum).split('').forEach(digit => tempSum += parseInt(digit, 10));
                sum = tempSum;
            }
            return sum;
        }

        function calculatePersonalDayNumber(birthDateStr) {
            // Personal Day = Month + Day + Current Year + Current Month + Current Day (Simplified: Month + Day + Current Year reduced)
            // Common method: Month of birth + Day of birth + Current Year, reduced to single digit, then added to current month/day.
            // Let's use a standard Personal Year + Current Day calculation for simplicity.
            
            const today = new Date();
            const currentYear = today.getFullYear();
            const currentMonth = today.getMonth() + 1;
            const currentDay = today.getDate();
            
            const birthMonth = parseInt(birthDateStr.substring(4, 6));
            const birthDay = parseInt(birthDateStr.substring(6, 8));

            let sum = birthMonth + birthDay + currentYear + currentMonth + currentDay;
             while (sum > 9) {
                let tempSum = 0;
                String(sum).split('').forEach(digit => tempSum += parseInt(digit, 10));
                sum = tempSum;
            }
            return sum;
        }

        // --- Logic: Tarot ---
        const majorArcana = [
            "0. The Fool (광대)", "I. The Magician (마법사)", "II. The High Priestess (고위 여사제)", 
            "III. The Empress (여황제)", "IV. The Emperor (황제)", "V. The Hierophant (교황)", 
            "VI. The Lovers (연인)", "VII. The Chariot (전차)", "VIII. Strength (힘)", 
            "IX. The Hermit (은둔자)", "X. Wheel of Fortune (운명의 수레바퀴)", "XI. Justice (정의)", 
            "XII. The Hanged Man (매달린 사람)", "XIII. Death (죽음)", "XIV. Temperance (절제)", 
            "XV. The Devil (악마)", "XVI. The Tower (탑)", "XVII. The Star (별)", 
            "XVIII. The Moon (달)", "XIX. The Sun (태양)", "XX. Judgement (심판)", "XXI. The World (세계)"
        ];

        function drawTarotCard() {
            const randomIndex = Math.floor(Math.random() * majorArcana.length);
            return majorArcana[randomIndex];
        }

        // --- Logic: I Ching ---
        let currentHexagram = []; 

        function generateHexagramLines() {
            const lines = [];
            for (let i = 0; i < 6; i++) {
                lines.push(Math.random() < 0.5 ? 0 : 1);
            }
            return lines;
        }

        function drawHexagramVisual(lines) {
            const container = document.getElementById('hexagramVisual');
            container.innerHTML = '';
            // Draw visual minified
            for (let i = 5; i >= 0; i--) {
                const isYang = lines[i] === 1;
                const lineDiv = document.createElement('div');
                lineDiv.style.height = "4px";
                lineDiv.style.marginBottom = "2px";
                lineDiv.style.width = "40px";
                lineDiv.style.backgroundColor = "#5d4037";
                lineDiv.style.borderRadius = "1px";
                
                if (!isYang) {
                    // Create gap for Yin
                    lineDiv.style.background = "linear-gradient(to right, #5d4037 40%, transparent 40%, transparent 60%, #5d4037 60%)";
                }
                container.appendChild(lineDiv);
            }
        }

        // --- API & Retry Logic ---
        const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

        async function fetchWithRetry(url, options, retries = 5, initialDelay = 1000) {
            let attempt = 0;
            let delay = initialDelay;

            while (attempt <= retries) {
                try {
                    const response = await fetch(url, options);
                    if (response.status === 429) throw new Error("429_TOO_MANY_REQUESTS");
                    if (!response.ok) throw new Error(`HTTP_ERROR_${response.status}`);
                    return response;
                } catch (error) {
                    if (error.message === "429_TOO_MANY_REQUESTS" && attempt < retries) {
                        const loadingText = document.getElementById('loadingText');
                        if (loadingText) loadingText.textContent = `대기 중입니다... (${attempt + 1}/${retries})`;
                        await wait(delay);
                        attempt++;
                        delay *= 2;
                    } else {
                        throw error;
                    }
                }
            }
        }

        async function getInterpretation(data) {
            const { name, birthDate, birthTime, query, hexagramLines, tarotCard, lifePath, personalDay } = data;
            
            // Hexagram text description
            const linesDesc = hexagramLines.map((val, idx) => `효 ${idx + 1} (아래에서 위로): ${val === 1 ? '양(Solid)' : '음(Broken)'}`).join('\n');

            // Constructing the Prompt based on User's Request
            const prompt = `
당신은 대한민국 최고의 운세 전략가입니다. 아래 데이터를 바탕으로 ${name}님을 위한 오늘 하루 실전 가이드를 작성해주세요.

[입력 데이터]
- 이름: ${name}
- 생년월일시: ${birthDate} ${birthTime}
- 고민/질문: ${query || "오늘의 종합 운세"}
- 🔢 수비학(계산됨): 운명수 ${lifePath} / 일운수 ${personalDay}
- 🃏 타로카드(뽑힘): ${tarotCard}
- ☯️ 주역 괘(생성됨): 
${linesDesc}

[분석 지시사항]
1. 사주(Four Pillars), 기문둔갑(Qimen Dunjia), 점성술(Astrology) 정보는 위 생년월일시를 바탕으로 당신이 전문 지식을 활용해 직접 분석/계산하여 채워 넣으세요.
2. 주역 괘는 위 효(Line) 정보를 바탕으로 64괘 중 무엇인지 식별하고 해석하세요.

[출력 형식 및 작성 원칙 (반드시 준수)]
- 문장은 짧고 명확하게 (한 문장 = 1개 메시지)
- 추상적 표현 금지, 구체적 시간/행동만 제시
- 비유와 실생활 예시 필수
- 총 2000자 이상 풍부하게 작성
- 답변 첫머리에 "알겠습니다" 등의 서론을 쓰지 말고 바로 아래 제목부터 시작할 것.

---

## 🎯 오늘의 종합 운세

**점수:** ___/100점

**한 줄 요약:** (오늘을 한 문장으로)

오늘의 에너지를 비유하자면 "___"에 비유할 수 있습니다.
전반적으로 ___한 흐름이 예상됩니다. (사주 일간과 기문둔갑의 흐름을 종합하여 서술)

**영역별 운세:**
- 애정운: ___/100 - (한 줄 조언)
- 재물운: ___/100 - (한 줄 조언)
- 사업운: ___/100 - (한 줄 조언)
- 건강운: ___/100 - (한 줄 조언)

---

## 🔢 수비학 × 사주 분석

**당신의 운명수 ${lifePath}:** (타고난 성향 1문장)
**오늘의 일운수 ${personalDay}:** (오늘의 에너지 1문장)

**둘의 조합이 말하는 것:**
운명수 ${lifePath}는 ___한 성향이지만, 오늘의 일운수 ${personalDay}는 ___를 요구합니다.
마치 ___과 같은 상황입니다.

**사주와의 연결:**
일간(Day Master)은 ___ (예: 갑목, 병화 등)이며 ___한 기질입니다.
오늘은 이 기질이 ___ 방향으로 작용합니다.

**실전 적용:**
예를 들어, 평소 ___한 당신이 오늘은 ___하면 좋습니다.
구체적으로 ___할 때 ___하세요.

---

## ⚡ 기문둔갑 시공간 전략

**오늘의 골든타임:**
- 오전: ___시~___시 (이유: ___)
- 오후: ___시~___시 (이유: ___)

**이 시간에 할 일:**
골든타임에는 마치 ___처럼 ___하세요.
예: 중요한 미팅은 오전 ___시에, 창의적 작업은 오후 ___시에.

**길방(Lucky Direction) 활용법:**
(생문, 개문, 휴문 중 오늘의 길방 분석)
이 방향은 ___ 에너지가 강합니다.
실천 예시: 책상을 이 방향으로 향하게 앉거나, 이 방향으로 산책하세요.

**피해야 할 시간:**
오후 ___시~___시는 에너지가 정체됩니다.
이 시간에는 중요한 결정이나 새로운 시작을 피하세요.

---

## 💌 주역과 타로의 메시지

**주역 (Hexagram):**
(식별된 괘 이름) - 이 괘는 ___을 상징합니다.
오늘 상황에 비유하면, "___"입니다.
핵심 조언: (1문장)

**타로 (${tarotCard}):**
이 카드는 ___를 의미합니다.
당신의 상황에 적용하면, "___"라는 뜻입니다.
핵심 조언: (1문장)

**두 점술의 공통 메시지:**
주역과 타로 모두 "___"를 강조합니다.
마치 ___와 같은 상황이니, ___하세요.

---

## 📋 오늘의 행동 강령

### ✅ 꼭 해야 할 일 3가지

1. **오전 ___시경:** (기문둔갑 길방) 방향에서 ___하기
   - 예: 동쪽 창문 앞에서 10분간 스트레칭, 또는 동쪽 카페에서 업무 시작

2. **점심시간:** ___색 계열 음식 먹기
   - 예: (사주 용신에 맞는 색상 음식 추천)
   - 이유: 일운수 ${personalDay} 에너지 보충

3. **저녁 ___시 전:** 오늘의 성과를 ___에 기록하기
   - 예: 일기장에 감사한 일 3가지 쓰기, 또는 목표 진행상황 체크

### ❌ 절대 피해야 할 일 3가지

1. **오후 ___시~___시:** 중요한 금전 거래나 계약 피하기
   - 이유: 기문둔갑상 이 시간은 재물운이 약함
   - 대신: 이 시간에는 가벼운 업무나 정리 작업만

2. **___방향으로의 이동:** 불필요한 ___쪽 이동 자제
   - 이유: 주역 괘상 이 방향은 장애물 있음
   - 대신: 급한 일 아니면 다른 방향 선택

3. **타인과의 갈등:** 특히 ___한 사람과의 논쟁 피하기
   - 이유: 타로 카드가 관계 마찰 경고
   - 대신: 오늘은 경청하고, 내일 다시 대화

### 🍀 오늘의 행운 아이템

- **색상:** (사주의 부족한 기운을 채우거나 일운수와 조화되는 최적의 색상)
  → 추천 이유: (명확한 근거 제시)
  → 실천법: (옷, 소품, 인테리어 등 구체적 활용법)
  
- **숫자:** ${personalDay} (또는 오늘의 행운 숫자)
  → 활용법: (비밀번호, 시간, 개수 등 구체적 활용법)
  
- **음식:** (사주 일간의 에너지를 보강하는 음식)
  → 추천 메뉴: (점심/저녁 구체적 메뉴 추천)
  
- **방향:** (기문둔갑 길방)
  → 활용법: (이 방향으로의 산책, 여행, 자리 배치 등)

### 💡 추가 실전 팁

**만약 ___한 상황이 온다면:**
마치 ___처럼 ___하세요.
예: 갑자기 중요한 제안이 들어오면, 골든타임인 오전 ___시까지 기다렸다가 답하세요.

**하루를 마무리할 때:**
오늘 ___했다면 성공입니다.
내일은 일운수가 (다음 일운수)로 바뀌니, ___를 준비하세요.
            `;

            try {
                const response = await fetchWithRetry(
                    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`,
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            contents: [{ parts: [{ text: prompt }] }]
                        })
                    }
                );
                const result = await response.json();
                return result.candidates[0].content.parts[0].text;
            } catch (error) {
                console.error(error);
                if (error.message.includes("429")) {
                    throw new Error("접속자가 많아 분석이 지연되고 있습니다. 잠시 후 다시 시도해주세요.");
                } else {
                    throw new Error("운세 분석 중 오류가 발생했습니다.");
                }
            }
        }

        // --- Main Controller ---

        async function drawFortune() {
            const userName = document.getElementById('userName').value.trim();
            const birthDate = document.getElementById('birthDate').value.trim();
            const birthTime = document.getElementById('birthTime').value;
            const query = document.getElementById('query').value.trim();
            
            const errorMsg = document.getElementById('errorMessage');
            const resultSection = document.getElementById('resultSection');
            const loading = document.getElementById('loading');
            const interpretationDiv = document.getElementById('interpretation');
            const drawBtn = document.getElementById('drawBtn');

            // Validation
            if (!userName) {
                errorMsg.textContent = "이름을 입력해주세요.";
                errorMsg.classList.remove('hidden');
                return;
            }
            if (!birthDate || birthDate.length !== 8 || isNaN(birthDate)) {
                errorMsg.textContent = "생년월일을 올바른 형식(YYYYMMDD)으로 입력해주세요.";
                errorMsg.classList.remove('hidden');
                return;
            }
            if (!birthTime) {
                errorMsg.textContent = "태어난 시간을 입력해주세요.";
                errorMsg.classList.remove('hidden');
                return;
            }

            // Prep UI
            errorMsg.classList.add('hidden');
            resultSection.classList.remove('hidden');
            loading.classList.remove('hidden');
            interpretationDiv.classList.add('hidden');
            interpretationDiv.innerHTML = '';
            drawBtn.disabled = true;
            drawBtn.classList.add('opacity-50', 'cursor-not-allowed');

            // 1. Calculate & Generate Data Locally
            const lifePath = calculateLifePathNumber(birthDate);
            const personalDay = calculatePersonalDayNumber(birthDate);
            const tarotCard = drawTarotCard();
            const hexagramLines = generateHexagramLines();

            // Display Local Data immediately
            document.getElementById('dispLifePath').textContent = lifePath;
            document.getElementById('dispTarot').textContent = tarotCard.split('(')[0]; // Show English name mostly
            drawHexagramVisual(hexagramLines);

            resultSection.scrollIntoView({ behavior: 'smooth' });

            // 2. Call AI for Deep Analysis
            try {
                const text = await getInterpretation({
                    name: userName,
                    birthDate,
                    birthTime,
                    query,
                    hexagramLines,
                    tarotCard,
                    lifePath,
                    personalDay
                });
                
                // Format Output
                const formattedText = text
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/---/g, '<hr class="my-6 border-stone-300">')
                    .replace(/\n/g, '<br>');

                interpretationDiv.innerHTML = formattedText;
                loading.classList.add('hidden');
                interpretationDiv.classList.remove('hidden');

            } catch (err) {
                loading.classList.add('hidden');
                errorMsg.textContent = err.message;
                errorMsg.classList.remove('hidden');
            } finally {
                drawBtn.disabled = false;
                drawBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                document.getElementById('loadingText').textContent = "운명 데이터를 분석 중입니다...";
            }
        }
    </script>
</body>
</html>