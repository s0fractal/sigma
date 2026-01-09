#![no_std]
/// 🛑 QUANTUM STATE: COLLAPSED FROM B.sigma
/// 🌊 FREQUENCY: rs | ENERGY: 2
pub fn B<A, B, C, F, G>(f: F, g: G) -> impl Fn(A) -> C
where
    F: Fn(B) -> C,
    G: Fn(A) -> B,
{
    move |x| f(g(x))
}
