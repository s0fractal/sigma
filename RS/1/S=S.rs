pub fn S<A, B, C, F, G>(f: F, g: G) -> impl Fn(A) -> C
where
    F: Fn(A) -> Box<dyn Fn(B) -> C>,
    G: Fn(A) -> B,
    A: Clone,
{
    move |x| f(x.clone())(g(x))
}
```
