#![no_std]
/// 🛑 QUANTUM STATE: COLLAPSED FROM E.sigma
/// 🌊 FREQUENCY: rs | ENERGY: 1
pub fn E<T, F>(eff: F) -> impl Fn(T) -> T 
where F: Fn(&T)
{
    move |x| { eff(&x); x }
}
