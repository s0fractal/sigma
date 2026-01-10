pub fn C<A, B, C, F>(f: F) -> impl Fn(B) -> Box<dyn Fn(A) -> C>
where
    F: Fn(A) -> Box<dyn Fn(B) -> C> + 'static,
{
    move |y| {
        let f = f.clone();
        Box::new(move |x| f(x)(y))
    }
}
```
