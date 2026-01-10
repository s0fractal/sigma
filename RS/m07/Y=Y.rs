// Fixed-point combinator in Rust (Symbolic)
pub fn Y<A, B, F>(f: F) -> impl Fn(A) -> B
where
    F: Fn(&dyn Fn(A) -> B) -> (dyn Fn(A) -> B),
{
    todo!()
}
