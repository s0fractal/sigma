pub fn K<A, B>(x: A) -> impl Fn(B) -> A + Clone 
where A: Clone
{
    move |_| x.clone()
}
```
