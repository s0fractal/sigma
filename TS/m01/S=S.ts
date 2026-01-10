export const S = <A, B, C>(f: (x: A) => (y: B) => C) => (g: (x: A) => B) => (x: A): C => f(x)(g(x));
