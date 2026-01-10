#![no_std]
/// 🛑 QUANTUM STATE: COLLAPSED FROM W.sigma
/// 🌊 FREQUENCY: rs | ENERGY: 2
pub fn W<A, B, F>(f: F) -> impl Fn(A) -> B
where F: Fn(A) -> Box<dyn Fn(A) -> B>, A: Clone
{
    move |x| f(x.clone())(x)
}
