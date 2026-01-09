// 🛑 QUANTUM STATE: COLLAPSED FROM B.sigma
// 🌊 FREQUENCY: ts | ENERGY: 2
export const B = <A, B, C>(f: (y: B) => C) => (g: (x: A) => B) => (x: A): C => f(g(x));
