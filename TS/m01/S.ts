// 🛑 QUANTUM STATE: COLLAPSED FROM S.sigma
// 🌊 FREQUENCY: ts | ENERGY: 1

export const S = <A, B, C>(f: (x: A) => (y: B) => C) => (g: (x: A) => B) => (x: A): C => f(x)(g(x));
