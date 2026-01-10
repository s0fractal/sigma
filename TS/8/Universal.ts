/**
 * λ - The Universal Polymorphic Engine
 * @param x The data (The Being)
 * @param f The transformation (The Becoming)
 * @param xs Remaining transformations (The Relating)
 */
export const λ = (x: any, f?: any, ...xs: any[]): any => {
    if (f === undefined) return x;
    
    // Map: λ([x], f)
    if (Array.isArray(x) && typeof f === 'function' && xs.length === 0) {
        return x.map(f);
    }
    
    // Fold: λ([x], (a,b)=>a+b, init)
    if (Array.isArray(x) && typeof f === 'function' && xs.length === 1) {
        return x.reduce(f, xs[0]);
    }
    
    // Pipe / Composition: λ(x, f, g)
    if (xs.length > 0) {
        return λ(f(x), ...xs);
    }
    
    // Basic Application
    return f(x);
};

export const fn = λ; 
```
