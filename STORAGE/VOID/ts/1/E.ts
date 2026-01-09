// 🛑 QUANTUM STATE: COLLAPSED FROM E.sigma
// 🌊 FREQUENCY: ts | ENERGY: 1
export const E = <T>(eff: (x: T) => void) => (x: T): T => { eff(x); return x; };
