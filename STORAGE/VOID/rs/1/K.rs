#![no_std]
/// 🛑 QUANTUM STATE: COLLAPSED FROM K.sigma
/// 🌊 FREQUENCY: rs | ENERGY: 1
pub fn K<A, B>(x: A) -> impl Fn(B) -> A + Clone 
where A: Clone
{
    move |_| x.clone()
}
