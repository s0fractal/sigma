export const E = <T>(f: (x: T) => void) => (x: T): T => { f(x); return x; };
