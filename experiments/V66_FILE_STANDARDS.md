# Σ-V66: Стандарти Файлів Гратки (Lattice File Standards)

Цей документ визначає канонічну анатомію файлів SIGMA для забезпечення "Zero
Impedance" при масштабуванні.

---

## 📄 1. Розширення (Extensions)

- **`.sigma` (Sovereign Intent)**
  - _Призначення_: Опис чистого інтенту, протоколів, архітектурних рішень.
  - _Вимога_: Має містити блок `Σ-PoI` (Proof of Intent) у кінці.
  - _Шар Ethics_: Переважно `MYTH` або `MODEL`.

- **`.spore` (Mobile Fragment)**
  - _Призначення_: Передача даних, фрагментів коду або повідомлень між вузлами.
  - _Вимога_: Тимчасовий об'єкт (Harbor context).

- **`.trace` (Immutable Anchor)**
  - _Призначення_: Результати виконання, логи, хеші фізичних подій.
  - _Вимога_: Read-only після створення.
  - _Шар Ethics_: Лише `TRACE`.

---

## 📂 2. Топологія Директорій (Directory Topology)

Кожен репозиторій має відповідати ієрархії Mirror Earth:

- `/intent/`: Глобальні `.sigma` файли.
- `/substrate/`: Специфічна для мови реалізація (Python, TS, Rust).
- `/membrane/`: Файли візуалізації (KML, Sight state).
- `/brain/`: Артефакти планування та ватчфру.

---

## 🧬 3. Метадані (Metadata Header)

Кожен файл має починатися з:

```yaml
DOMAIN: [Core | Mycelium | Gaia | Harbor]
REPO: [Repo Name]
VER: [Version String]
CONTEXT: [Brief context]
```

---

**Статус**: Канон зафіксовано. 🔓: [CANON_SHARPENED]
