/// Σ-GLYPH V1.9.1: Normative Math (Core Physics)
///
/// This module implements the bit-exact mathematical contracts defined in Section 3 of the Core Manifest.

/// Integer division with round-half-up (MUST).
/// Semantics: round-half-away-from-zero.
/// 
/// MUST: d MUST be > 0. Behavior for d <= 0 is undefined (implementation fault).
/// MUST: Implementations MUST promote n to a wider signed type before negation to avoid overflow (e.g., -(-32768)).
/// MUST: Promotion width MUST be at least i64.
/// Note: div_round_half_up(0, d) == 0; result sign follows n (away-from-zero for ties).
pub fn div_round_half_up(n: i32, d: i32) -> i32 {
    if d <= 0 {
        panic!("System Fault: div_round_half_up divisor MUST be positive (d={})", d);
    }
    
    // Convert to i64 to handle overflow during negation and calculation
    let n64 = n as i64;
    let d64 = d as i64;
    
    let s = if n64 < 0 { -1 } else { 1 };
    let a = n64.abs();
    
    let mut q = a / d64;
    let r = a % d64;
    
    if 2 * r >= d64 {
        q += 1;
    }
    
    (s * q) as i32
}

/// Clamps result to i16 range (Section 3.1).
pub fn clamp_i16(x: i32) -> i16 {
    if x < -32768 {
        -32768
    } else if x > 32767 {
        32767
    } else {
        x as i16
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_div_round_half_up() {
        // Basic positive
        assert_eq!(div_round_half_up(10, 3), 3);
        assert_eq!(div_round_half_up(11, 3), 4);
        
        // Ties (Round half up -> away from zero)
        assert_eq!(div_round_half_up(5, 2), 3);
        assert_eq!(div_round_half_up(-5, 2), -3);
        
        // Zero
        assert_eq!(div_round_half_up(0, 5), 0);
        
        // Overflow safety (i16 min)
        assert_eq!(div_round_half_up(-32768, 1), -32768);
    }

    #[test]
    fn test_clamp_i16() {
        assert_eq!(clamp_i16(40000), 32767);
        assert_eq!(clamp_i16(-40000), -32768);
        assert_eq!(clamp_i16(100), 100);
    }
}
