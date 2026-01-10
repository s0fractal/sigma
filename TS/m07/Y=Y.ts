type Func<A, B> = (x: A) => B;
type RecursiveFunc<A, B> = (f: Func<A, B>) => Func<A, B>;

export const Y = <A, B>(f: RecursiveFunc<A, B>): Func<A, B> => {
  const g = (h: any) => (x: A) => f(h(h))(x);
  return g(g);
};
