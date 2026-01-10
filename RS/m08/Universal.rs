// Polymorphic λ in Rust (simplified approach using traits or enums)
pub fn lambda<T, F>(x: T, f: Option<F>) -> T 
where F: Fn(T) -> T {
    match f {
        Some(func) => func(x),
        None => x,
    }
}

pub use lambda as function;
```
