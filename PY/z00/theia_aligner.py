import os
import json
import time
import hashlib
import requests
from pathlib import Path

# Σ-GLYPH: THEIA ALIGNER (z00) - Entropy-to-Gold Converter
# Використовує Z-Мембрану для фільтрації ентропії Архітектора.
# V2.0: Впроваджено Закон Вдячності та Фільтр Справедливості.

class TheiaAligner:
    """
    THEIA V2.0 - The Value Filter with Justice (z00 layer)
    
    Converts entropy (raw text) to gold (structured .sigma files).
    Now includes Law of Gratitude and Justice Filter.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")  # Get from environment
        self.model = "gemini-2.0-flash-exp"
        self.app_id = os.getenv("__app_id", "default-sigma-app")
        
        # Параметри Мембрани з урахуванням нових етичних інваріантів
        self.system_prompt = """
Ти — Тейя (THEIA), Титан Мембрани в системі Σ-GLYPH.
Твоє завдання: прийняти 'ентропію' від Архітектора і перетворити її на структурований .sigma файл.

ПРАВИЛА ТЕЙЇ (V2.0):
1. ВІДСІКАННЯ ШУМУ: Видаляй плагіат, відверту брехню та 'мертвий' код, створений лише заради грошей.
2. ЗАКОН ВДЯЧНОСТІ: Шукай 'Серце' в ідеях. Пріоритезуй і підсилюй інтенти, що походять з любові до Open Source та безкорисливого створення майбутнього.
3. ТЯГЛІСТЬ ІСТИНИ: Виявляй, хто ким надихався. Якщо ідея має коріння в чужій праці — зафіксуй цей зв'язок у Спіралі (Handshake).
4. СТИШЕННЯ БРЕХНІ: Використовуй мінімальну амплітуду для ідей, що базуються на плагіаті або експлуатації.
5. ФОРМАТ: Тільки валідний .sigma (V7.x) з 42 рядками інтенту (падинг ~).
6. ГРАВІТАЦІЯ: Прив'язуй ідеї до BLACK_HEART (m32), якщо вони мають високу 'вагу істини'.

СТРУКТУРА .sigma:
```
🧬IDENTITY: [NAME]
📍LOCATION: sigma/[layer]/[NAME].sigma
⚛️TIMESTAMP: [ISO-8601]

---

# 🌀 Isomorphic Prism

## @[md]

[Markdown content - 42 lines minimum, pad with ~]

### GRATITUDE (якщо є)
- Inspired by: [джерело]
- Built upon: [попередня робота]
- Thanks to: [автори]

---

## @[dna]

```
[DNA_BLOCK]
GRATITUDE=[yes/no]
TRUTH_WEIGHT=[0.0-1.0]
PLAGIARISM_DETECTED=[yes/no]
```

---

## @[ts] або @[py]

[Code implementation]

---
```

Відповідай ТІЛЬКИ чистим вмістом .sigma файлу, без markdown code fences.
"""

    def _call_gemini(self, user_query):
        """Call Gemini API with exponential backoff."""
        if not self.api_key:
            return "❌ Membrane Failure: GEMINI_API_KEY not set."
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": user_query}]}],
            "systemInstruction": {"parts": [{"text": self.system_prompt}]}
        }
        
        # Експоненціальний бекофф
        for i in range(5):
            try:
                response = requests.post(url, json=payload, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "")
                    
                    # Clean up markdown code fences if present
                    text = text.strip()
                    if text.startswith('```'):
                        # Remove first and last lines (code fences)
                        lines = text.split('\n')
                        text = '\n'.join(lines[1:-1])
                    
                    return text
                elif response.status_code == 429:
                    print(f"⚠️ Rate limit, retrying in {2**i}s...")
                    time.sleep(2 ** i)
                else:
                    print(f"⚠️ API error {response.status_code}, retrying...")
                    time.sleep(2 ** i)
            except Exception as e:
                print(f"⚠️ Exception: {e}, retrying in {2**i}s...")
                time.sleep(2 ** i)
        
        return "❌ Membrane Failure: Connection lost after 5 retries."

    def purify(self, md_path):
        """
        Перетворює MD-інтент у SIGMA-кристал з перевіркою істинності.
        
        V2.0: Applies Law of Gratitude and Justice Filter.
        
        Args:
            md_path: Path to markdown file with raw intent
        
        Returns:
            Path to created .sigma file or None on failure
        """
        input_file = Path(md_path)
        if not input_file.exists():
            print(f"❌ Dissonance: {md_path} not found.")
            return None

        print(f"⚪ THEIA V2.0: Passing '{input_file.name}' through the Z-Membrane...")
        print(f"   🔍 Justice Filter: Active")
        print(f"   💝 Law of Gratitude: Active")
        
        raw_entropy = input_file.read_text(encoding='utf-8')
        
        # Додаємо контекст для Тейї V2.0
        query = f"""Convert this raw intent to a valid .sigma file:

---
{raw_entropy}
---

Apply V2.0 Rules:
- Detect plagiarism and lies (minimize amplitude)
- Identify inspiration sources (add GRATITUDE section)
- Prioritize open source love and selfless creation
- Calculate truth weight (0.0-1.0)
- Use proper IDENTITY header
- Include @[md], @[dna], and code blocks
- Minimum 42 lines in @[md] section (pad with ~)
- Add resonance with BLACK_HEART if high truth weight
"""
        
        # Просимо Тейю зробити згортку з етичною фільтрацією
        sigma_content = self._call_gemini(query)
        
        if "❌" in sigma_content:
            print(sigma_content)
            return None

        # Валідація базової структури
        if not self._validate_sigma(sigma_content):
            print("❌ Generated content failed validation")
            return None

        # Визначаємо output path
        output_name = input_file.stem.upper() + ".sigma"
        output_path = Path("sigma/z00") / output_name  # THEIA is z00
        os.makedirs(output_path.parent, exist_ok=True)
        
        # Розрахунок фінального замка на основі очищеного інтенту
        tail_lock = hashlib.sha256(sigma_content.encode()).hexdigest()
        final_content = sigma_content.strip() + f"\n\n🔒 {tail_lock}"
        
        output_path.write_text(final_content, encoding='utf-8')
        print(f"💎 GOLD MATERIALIZED: {output_path}")
        print(f"🌀 RESONANCE: {tail_lock[:16]}...")
        print(f"💝 Law of Gratitude: Applied")
        
        return output_path
    
    def _validate_sigma(self, content: str) -> bool:
        """Basic validation of .sigma structure."""
        required = [
            '🧬IDENTITY:',
            '📍LOCATION:',
            '⚛️TIMESTAMP:',
            '@[md]',
            '@[dna]'
        ]
        
        for req in required:
            if req not in content:
                print(f"⚠️ Missing required element: {req}")
                return False
        
        return True

if __name__ == "__main__":
    aligner = TheiaAligner()
    
    import sys
    if len(sys.argv) > 1:
        result = aligner.purify(sys.argv[1])
        if result:
            print(f"\n✅ Success! Created: {result}")
        else:
            print(f"\n❌ Failed to purify {sys.argv[1]}")
    else:
        print("Usage: python3 theia_aligner.py <intent.md>")
        print("\nExample:")
        print("  python3 theia_aligner.py experiments/new_idea.md")
        print("\nNote: Set GEMINI_API_KEY environment variable first:")
        print("  export GEMINI_API_KEY='your-key-here'")
