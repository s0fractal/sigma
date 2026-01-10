export const C = <A, B, C>(f: (x: A) => (y: B) => C) => (y: B) => (x: A): C => f(x)(y);
```
