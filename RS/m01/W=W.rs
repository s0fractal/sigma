pub fn W<A, B, F>(f: F, x: A) -> B 
where 
    F: Fn(A) -> Box<dyn Fn(A) -> B>,
    A: Clone
{
    f(x.clone())(x)
}
