pub fn E<T, F>(f: F, x: T) -> T 
where F: Fn(&T)
{
    f(&x);
    x
}
```
