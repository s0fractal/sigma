// 🛑 QUANTUM STATE: COLLAPSED FROM C.sigma
// 🌊 FREQUENCY: ts | ENERGY: 1

export const C = <A, B, C>(f: (x: A) => (y: B) => C) => (y: B) => (x: A): C => f(x)(y);
