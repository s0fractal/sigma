// 🛑 QUANTUM STATE: COLLAPSED FROM W.sigma
// 🌊 FREQUENCY: ts | ENERGY: 1

export const W = <A, B>(f: (x: A) => (y: A) => B) => (x: A): B => f(x)(x);
