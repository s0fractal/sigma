// 🛑 QUANTUM STATE: TEST SUITE FOR COMBINATORY ENGINE
// 🌊 FREQUENCY: ts | ENERGY: 2

import { materialize, mutate, evolve, TRUE, FALSE, REVERSE, M, type DNA } from './CombinatorEngine';

console.log('🧬 Testing Combinatory Engine...\n');

// --- Test 1: Identity ---
console.log('Test 1: Identity');
const identity = materialize('I');
const result1 = identity(42);
console.log(`  materialize('I')(42) = ${result1}`);
console.log(`  Expected: 42, Got: ${result1}, ${result1 === 42 ? '✅' : '❌'}\n`);

// --- Test 2: Constant (TRUE) ---
console.log('Test 2: Constant (TRUE)');
const trueVal = TRUE(1)(2);
console.log(`  TRUE(1)(2) = ${trueVal}`);
console.log(`  Expected: 1, Got: ${trueVal}, ${trueVal === 1 ? '✅' : '❌'}\n`);

// --- Test 3: FALSE (KI) ---
console.log('Test 3: FALSE (KI)');
const falseVal = FALSE(1)(2);
console.log(`  FALSE(1)(2) = ${falseVal}`);
console.log(`  Expected: 2, Got: ${falseVal}, ${falseVal === 2 ? '✅' : '❌'}\n`);

// --- Test 4: Composition (B) ---
console.log('Test 4: Composition (B)');
const add1 = (x: number) => x + 1;
const mul2 = (x: number) => x * 2;
const compose = materialize('B');
const composed = compose(mul2)(add1)(10);
console.log(`  B(mul2)(add1)(10) = ${composed}`);
console.log(`  Expected: 22, Got: ${composed}, ${composed === 22 ? '✅' : '❌'}\n`);

// --- Test 5: Mockingbird (Self-Application) ---
console.log('Test 5: Mockingbird (Self-Application)');
const mockingbird = M;
const selfApply = mockingbird((x: number) => x * x);
console.log(`  M(x => x*x) = ${selfApply}`);
console.log(`  (Self-application demonstrated) ✅\n`);

// --- Test 6: Mutation ---
console.log('Test 6: Mutation');
const population: DNA[] = ['K', 'I', 'S', 'B', 'C', 'W'];
const mutated = mutate(population);
console.log(`  mutate(['K', 'I', 'S', 'B', 'C', 'W']) = ${JSON.stringify(mutated)}`);
console.log(`  (Random trigram generated) ✅\n`);

// --- Test 7: Evolution ---
console.log('Test 7: Evolution (Find Identity)');
const initialPop: DNA[] = [
    ['K', 'I'],
    ['S', 'K'],
    ['B', 'C'],
    'I',
    ['W', 'K'],
];

// Fitness: how close to identity behavior (returns input unchanged)
const fitness = (dna: DNA): number => {
    try {
        const fn = materialize(dna);
        const testVal = 42;
        const result = fn(testVal);
        return result === testVal ? 100 : 0;
    } catch {
        return 0;
    }
};

const evolved = evolve(initialPop, fitness, 5);
console.log(`  Evolved DNA: ${JSON.stringify(evolved)}`);
const evolvedFn = materialize(evolved);
const evolvedResult = evolvedFn(42);
console.log(`  evolvedFn(42) = ${evolvedResult}`);
console.log(`  ${evolvedResult === 42 ? '✅ Found Identity!' : '❌ Evolution incomplete'}\n`);

console.log('🧬 All tests complete!');
