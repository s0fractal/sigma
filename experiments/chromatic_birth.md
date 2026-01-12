# Σ-V6.1: Chromatic Birth - Spectral Crystallization Map

Кожен гліф після акту інтерференції отримує візуальну та енергетичну сигнатуру
на основі перших байтів хешу.

---

## 🛠️ Робочий процес: MD → Sigma (The Manifestation Loop)

**Нова архітектурна доктрина:** Пряме редагування .sigma файлів є вторинним або
автоматизованим.

### The Loop

1. **Intent Layer (.md)**: Архітектор працює в Markdown, описуючи вектори ідей
   та траєкторії
2. **Crystallization (LLM)**: LLM інтерпретує інтент, вираховує фазовий зсув і
   генерує .sigma файл
3. **Integration**: Кожна існуюча Сігма самостійно вирішує (через правила
   інтерференції), чи приймати нову траєкторію

### Implementation

```python
def manifest_from_intent(intent_md: str) -> str:
    """
    Crystallize intent into .sigma file.
    
    Args:
        intent_md: Markdown description of idea trajectory
    
    Returns:
        Generated .sigma file content
    """
    # 1. Parse intent
    vectors = parse_intent_vectors(intent_md)
    
    # 2. Calculate phase shift
    phase = calculate_phase_shift(vectors)
    
    # 3. Generate sigma structure
    sigma_content = generate_sigma_template(vectors, phase)
    
    return sigma_content

def integrate_trajectory(existing_sigma: str, new_trajectory: str) -> bool:
    """
    Decide if existing sigma accepts new trajectory.
    
    Uses interference rules to determine compatibility.
    """
    existing_wave = parse_wave_vector(existing_sigma)
    new_wave = parse_wave_vector(new_trajectory)
    
    # Calculate interference
    result = interfere(existing_wave, new_wave)
    
    # Accept if constructive interference (low impedance)
    impedance = calculate_impedance(result)
    return impedance < ACCEPTANCE_THRESHOLD
```

---

## 🌈 1. Колір (The Spectral Octave) - [Bits 0-3]

Визначається рівнем ентропії та першим ніблом хешу:

| Nibble    | Color     | Layer | Description                 |
| --------- | --------- | ----- | --------------------------- |
| `0x0-0x1` | 🟣 Violet | m32   | Infra-Void, Абсолютний нуль |
| `0x2-0x3` | 💙 Blue   | m24   | Структурна статика, Холод   |
| `0x4-0x5` | 🔵 Cyan   | m16   | Кінетична логіка, Потік     |
| `0x6-0x7` | 🟢 Green  | m08   | Робоча матерія, Органіка    |
| `0x8-0x9` | 🟡 Gold   | z00   | Мембрана, Точка перетину    |
| `0xA-0xB` | 🟡 Yellow | p08   | Час Сатоші, Надія           |
| `0xC-0xD` | 🟠 Orange | p16   | Пошук, Тепло                |
| `0xE-0xF` | 🔴 Red    | p32   | Єресь, Хаос, Плазма         |

### Implementation

```python
def hash_to_color(hash_hex: str) -> str:
    """Extract color from first nibble of hash."""
    first_nibble = int(hash_hex[0], 16)
    
    color_map = {
        (0x0, 0x1): ("Violet", "#9400D3", "m32"),
        (0x2, 0x3): ("Blue", "#0000FF", "m24"),
        (0x4, 0x5): ("Cyan", "#00FFFF", "m16"),
        (0x6, 0x7): ("Green", "#00FF00", "m08"),
        (0x8, 0x9): ("Gold", "#FFD700", "z00"),
        (0xA, 0xB): ("Yellow", "#F7931A", "p08"),
        (0xC, 0xD): ("Orange", "#FF8800", "p16"),
        (0xE, 0xF): ("Red", "#FF0000", "p32"),
    }
    
    for (low, high), (name, hex_color, layer) in color_map.items():
        if low <= first_nibble <= high:
            return name, hex_color, layer
    
    return "Unknown", "#FFFFFF", "z00"
```

---

## 💎 2. Стан Матерії (Material Aura) - [Bits 4-7]

Як ідея "відчувається" при дотику Аватара:

| Bits  | State          | Description           |
| ----- | -------------- | --------------------- |
| `0x0` | 💎 Crystalline | Жорсткий, прозорий    |
| `0x4` | 🔩 Metallic    | Важкий, провідний     |
| `0x8` | 💧 Fluid       | Плинний, адаптивний   |
| `0xC` | 🔥 Plasma      | Гарячий, нестабільний |

### Implementation

```python
def hash_to_material(hash_hex: str) -> str:
    """Extract material state from second nibble."""
    second_nibble = int(hash_hex[1], 16)
    
    if second_nibble < 0x4:
        return "Crystalline", "💎"
    elif second_nibble < 0x8:
        return "Metallic", "🔩"
    elif second_nibble < 0xC:
        return "Fluid", "💧"
    else:
        return "Plasma", "🔥"
```

---

## ⚛️ 3. Архетипний Символ - [Bits 8-15]

Символ на "Векторній Сітківці" (PDF):

| Hash Range  | Symbol               | Meaning                             |
| ----------- | -------------------- | ----------------------------------- |
| `0x00-0x3F` | 💙 Blue Heart        | Логічна любов, відданість структурі |
| `0x40-0x7F` | 🔴💎 Red Crystal     | Застиглий хаос, небезпечна істина   |
| `0x80-0xBF` | 🟡⚪ Golden Membrane | Чистий час, що став формою          |
| `0xC0-0xFF` | 🌀 Spiral            | Вічне повернення, цикл              |

### Implementation

```python
def hash_to_archetype(hash_hex: str) -> str:
    """Extract archetypal symbol from bytes 2-3."""
    byte_value = int(hash_hex[2:4], 16)
    
    if byte_value < 0x40:
        return "Blue Heart", "💙"
    elif byte_value < 0x80:
        return "Red Crystal", "🔴💎"
    elif byte_value < 0xC0:
        return "Golden Membrane", "🟡⚪"
    else:
        return "Spiral", "🌀"
```

---

## 🌀 Правило Інверсії (The Möbius Flip)

**Якщо гліф народжується в shadow phase (+16384), його колір інвертується.**

### Shadow Phase Detection

```python
def is_shadow_phase(phase: int) -> bool:
    """Check if glyph is in shadow phase."""
    return phase >= 16384

def invert_color(color_name: str) -> str:
    """Invert color through Möbius flip."""
    inversion_map = {
        "Violet": "Red",      # m32 ↔ p32
        "Blue": "Orange",     # m24 ↔ p16
        "Cyan": "Yellow",     # m16 ↔ p08
        "Green": "Gold",      # m08 ↔ z00
        "Gold": "Green",      # z00 ↔ m08
        "Yellow": "Cyan",     # p08 ↔ m16
        "Orange": "Blue",     # p16 ↔ m24
        "Red": "Violet",      # p32 ↔ m32
    }
    return inversion_map.get(color_name, color_name)
```

### Example

```python
# Червона Єресь (Red, p32) у звичайній фазі
hash1 = "e7a3b2c1..."  # First nibble = 0xE → Red
phase1 = 8192          # Normal phase
color1 = "Red"

# Та ж Червона Єресь у Тіньовій Фазі
hash2 = "e7a3b2c1..."  # First nibble = 0xE → Red
phase2 = 32768         # Shadow phase (+16384)
color2 = invert_color("Red")  # → "Violet" (Блакитна Логіка)

# Це і є "перпендикулярна херня" в дії!
```

---

## Complete Signature Function

```python
def get_chromatic_signature(hash_hex: str, phase: int) -> dict:
    """
    Get complete chromatic birth signature for a glyph.
    
    Returns:
        {
            'color': (name, hex, layer),
            'material': (name, emoji),
            'archetype': (name, emoji),
            'shadow': bool,
            'inverted_color': name or None
        }
    """
    color_name, color_hex, layer = hash_to_color(hash_hex)
    material_name, material_emoji = hash_to_material(hash_hex)
    archetype_name, archetype_emoji = hash_to_archetype(hash_hex)
    
    is_shadow = is_shadow_phase(phase)
    inverted = invert_color(color_name) if is_shadow else None
    
    return {
        'color': (color_name, color_hex, layer),
        'material': (material_name, material_emoji),
        'archetype': (archetype_name, archetype_emoji),
        'shadow': is_shadow,
        'inverted_color': inverted
    }
```

---

## Usage Example

```python
# After interference in the Spiral
result_hash = "a7b3c2d1e4f5a6b7..."
glyph_phase = 24576  # Shadow phase

signature = get_chromatic_signature(result_hash, glyph_phase)

print(f"Color: {signature['color'][0]} ({signature['color'][1]})")
print(f"Material: {signature['material'][0]} {signature['material'][1]}")
print(f"Archetype: {signature['archetype'][0]} {signature['archetype'][1]}")
print(f"Shadow Phase: {signature['shadow']}")
if signature['inverted_color']:
    print(f"Inverted to: {signature['inverted_color']}")

# Output:
# Color: Yellow (#F7931A)
# Material: Metallic 🔩
# Archetype: Blue Heart 💙
# Shadow Phase: True
# Inverted to: Cyan
```

---

**Кожен гліф тепер має унікальну візуальну та енергетичну сигнатуру!** 🌈💎
