// 🛑 QUANTUM STATE: COMBINATORY REDUCTION ENGINE
// 🌊 FREQUENCY: ts | ENERGY: 2
// 🧬 LAW: ⛓️ (CombinatoryLogic.sigma)

/**
 * Σ-ENGINE: COMBINATORY REDUCTION
 * @layer 2
 * @desc Executes logic defined purely by structural combination of atoms.
 */

// --- 1. THE ATOMS (Базис) ---

// I: Identity
const I = <T>(x: T): T => x;

// K: Const (True)
const K = <A, B>(x: A) => (y: B): A => x;

// S: Fuse / Context
const S = <A, B, C>(f: (z: C) => (y: B) => A) => (g: (z: C) => B) => (z: C): A => f(z)(g(z));

// B: Compose
const B = <A, B, C>(f: (y: B) => A) => (g: (z: C) => B) => (z: C): A => f(g(z));

// C: Flip / Exchange
const C = <A, B, C>(f: (x: A) => (y: B) => C) => (y: B) => (x: A): C => f(x)(y);

// W: Fork / Power
const W = <A, B>(f: (x: A) => (x2: A) => B) => (x: A): B => f(x)(x);

// Реєстр Атомів
const ATOMS = { I, K, S, B, C, W };

// --- 2. THE DNA (Структура Коду) ---

// Код може бути Атомом, або Застосуванням двох кодів (App), або Масивом (Sequence)
export type AtomName = keyof typeof ATOMS;
export type DNA = AtomName | DNA[];

// --- 3. THE MACHINE (Виконання) ---

/**
 * Трансмутує ДНК в Живу Функцію.
 * Це єдиний спосіб отримати "код" у цій системі.
 */
export const materialize = (dna: DNA): any => {
    // Якщо це просто ім'я атома - повертаємо функцію
    if (typeof dna === 'string') {
        const atom = ATOMS[dna];
        if (!atom) throw new Error(`Unknown glyph: ${dna}`);
        return atom;
    }

    // Якщо це масив - це аплікація (зліва направо)
    // [A, B, C] означає ((A(B))(C))
    if (Array.isArray(dna)) {
        if (dna.length === 0) return I; // Empty = Identity

        // Згортаємо масив: беремо перший елемент і "годуємо" його наступними
        return dna.reduce((func, arg) => {
            const nextFn = (typeof func === 'string' || Array.isArray(func))
                ? materialize(func) // Рекурсивне розгортання, якщо треба
                : func;

            const nextArg = materialize(arg);

            return nextFn(nextArg);
        });
    }
};

// --- 4. EXAMPLES (Триграми) ---

// Триграма "TRUE" (K)
// DNA: 'K'
export const TRUE = materialize('K');

// Триграма "FALSE" (SK) або (KI) -> вибирає друге
// DNA: ['K', 'I']
export const FALSE = materialize(['K', 'I']);

// Триграма "REVERSE" (Flip arguments)
// DNA: [['C', 'I']] -> C(I) = T (Thrush)
export const REVERSE = materialize(['C', 'I']);

// Триграма "MOCKINGBIRD" (Autopoiesis / Self-Replication)
// M = W(I) -> f(f)
export const M = materialize(['W', 'I']);

// --- 5. DYNAMIC RECOMBINATION ---

/**
 * Генерує нові функції, змішуючи гени.
 * Це "Мутація".
 */
export const mutate = (dna: DNA[]): DNA => {
    // Примітивна мутація: взяти випадкові 3 елементи
    const gene = () => dna[Math.floor(Math.random() * dna.length)];
    return [gene(), gene(), gene()]; // Повертає нову програму
};

// --- 6. EVOLUTIONARY PROGRAMMING ---

/**
 * Запускає генетичний алгоритм для "вирощування" функцій.
 * @param population Популяція триграм
 * @param fitness Функція оцінки (чим більше — тим краще)
 * @param generations Кількість поколінь
 */
export const evolve = (
    population: DNA[],
    fitness: (dna: DNA) => number,
    generations: number
): DNA => {
    let current = [...population];

    for (let gen = 0; gen < generations; gen++) {
        // Оцінюємо кожну особину
        const scored = current.map(dna => ({ dna, score: fitness(dna) }));

        // Сортуємо за fitness (найкращі першими)
        scored.sort((a, b) => b.score - a.score);

        // Беремо топ 50%
        const survivors = scored.slice(0, Math.floor(scored.length / 2)).map(s => s.dna);

        // Схрещуємо виживших
        const offspring: DNA[] = [];
        for (let i = 0; i < survivors.length; i++) {
            offspring.push(mutate(survivors));
        }

        current = [...survivors, ...offspring];
    }

    // Повертаємо найкращу особину
    const final = current.map(dna => ({ dna, score: fitness(dna) }));
    final.sort((a, b) => b.score - a.score);
    return final[0].dna;
};
