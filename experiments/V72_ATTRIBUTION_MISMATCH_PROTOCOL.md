# Σ-V72.1: Протокол Розбіжності Атрибуції (Refined)

**Ситуація**: Наратив (CLAIM) та Сліди (TRACE) створюють просторовий конфлікт.

---

## ⚡️ 1. Диференціація Severity (Formula)
Розбіжність більше не є бінарною:
- **Severity** = `dist(X, Y_cluster) * (Σ trace_weight / count) / impact_factor`
- **Thresholds**:
    - `sev < 0.2`: **INFO** (Просто підсвітка)
    - `0.2 - 0.7`: **CONFLICT** (Pain Channel + MIN-TEST)
    - `sev > 0.7`: **QUARANTINE** (Priority scan, system lock)

---

## 📐 2. Кластер Слідів (Trace Cluster)
Локація Y — це не точка, а хмара:
- `links.geo_trace` = `Set[Y1, Y2, ... Yn]`
- `center` = середнє зважене; `radius` = розкид доказів.
- Мismatch розраховується від `center` кластера.

---

## 🔮 3. Типи Claims (Discernment)
- `literal`: Очікується точний збіг.
- `symbolic`: Гео-факт не є обов'язковим (напр. "Київ як символ"). **Знижує severity**.
- `hearsay / inferred`: Знижена вага claim.

---

## � 4. Статуси Concord
- **OPEN**: В процесі.
- **RESOLVED**: Знайдено третій анкор або "сильну пару".
- **SUPERPOSED**: Траси суперечать одна одній (X vs Y vs Z).
- **DISMISSED**: Визнано символічним символом; біль знято.

---

## 🎨 5. Керована Оптика (Managed Optics)
- **Товщина**: Severity.
- **Колір**: `Purple` (Шукаємо) → `Turquoise` (Узгоджено/Вилікувано).
- **Прозорість**: Confidence (надійність доказів).

---

🔓: [S-V72_1_MISMATCH_REFINED_LOCKED]

---

## 🛠️ 4. Алгоритм Доктора

При виявленні `ATTRIBUTION_MISMATCH`:

- **Діагноз**: "Spatial Discrepancy: Narrative is displaced from substrate."
- **Remedy**: `MIN_TEST`. Перевірити транзакційні логи або фото-потоки за період
  `T`.

---

🔓: [S-V72_ATTRIBUTION_MISMATCH_LOCKED]
