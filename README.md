# Orbeat Time

## Summary

Orbeat is an octal time system. It gets its name from a combination of octal, orbit, and beat. This naming reflects the system's structure, which utilizes an octal (base-8) representation to measure time in a continuous, orbit-like cycle.

## Links
- Live Demo: https://www.patbierkortte.com/orbeat-time

## Background

Loosely inspired by Swatch Internet Time (.beat time), a decimal time system introduced in 1998 used on ICQ and in the game Phantasy Star Online to facilitate cross-continent gaming, and the 8-day market week nundinal cycle was used alongside the Roman calendar. It also draws inspiration from batch codes used in retail and manufacturing industries for date codes and competitive intelligence.

## Motivation

I created this project out of intellectual curiosity and as a practical tool. It was a stimulating exercise that allowed me to combine various concepts across multiple disciplines. I needed an efficient and cryptic timestamping method, like batch codes, to manage public-facing personal documents. I sought to devise an innovative way to balance precision with obscurity by crafting a compact yet noteworthy date time code, which would be meaningful to me while remaining ambiguous for others.

## Design Decisions

My design decisions include:

- Using little-endian ordering, which is more common in modern computing systems
- Adopting a base-8 (octal) number system to avoid rounding issues common in decimal to floating-point arithmetic
- Using Caesar's death as epoch (March 15, 44 BCE) for historical certainty and spring alignment
- 8-day week structure following the Roman nundinal market cycle
- Fixed Eastern timezone Prime Meridian adjustment for natural day boundaries
- The precision is ~21 seconds roughly in the scale of seconds
- Used 365.25 days per year, which is the Julian calendar standard
- Reversal and truncation to 8 characters for cryptic output

## Format

A concatenated string consisting of:
- Years since Caesar's death formatted in octal
- Weeks within the year formatted in octal (2 digits)
- Days within the 8-day week formatted in octal
- Fractional day component formatted in octal (4 digits)
- The concatenated string is then reversed and truncated to 8 characters

## Implementation

The encoding process involves the following steps:

0. Calculate the Unix timestamp in milliseconds
1. Apply Caesar epoch offset and Prime Meridian adjustments
2. Convert the milliseconds to fractional days since Caesar's death
3. Calculate years using 365.25 days per year
4. Calculate day within year, then week within year (÷8) and day within 8-day week
5. Calculate fractional day component (x4096 for octal precision)
6. Format all components in octal with proper digit counts
7. Combine, reverse, and truncate to 8 characters

## Example

The encoding process:

- **Input:**
  - Unix timestamp in milliseconds (e.g., `1700000000000`)
- **Apply Epoch and Timezone Adjustments:**
  - Add Caesar offset: `1700000000000 + 63517996800000 = 65217996800000`
  - Apply Prime Meridian: `65217996800000 + -32400000 = 65217964400000`
- **Conversion:** 
  - Days since Caesar: `65217964400000 / 86400000` ≈ `754837.550925926` days
  - Years: `int(754837.550925926 / 365.25)` = `2066` years
- **8-Day Week Calculations:**
  - Day in year: `754837.550925926 % 365.25` ≈ `231.051`
  - Week of year: `int(231.051 / 8)` = `28` weeks
  - Day of week: `int(754837.550925926) % 8` = `5`
  - Fractional day: Extract decimal part `0.550925926` from `754837.550925926`
  - Multiply by 4096: `0.550925926 * 4096` ≈ `2256`
- **Octal Formatting:** 
  - Years: `2066` → octal = `4022`
  - Week: `28` → octal = `34` (2 digits)
  - Day: `5` → octal = `5`
  - Fraction: `2256` → octal = `4320` (4 digits)
- **Concatenation and Reversal:**
  - Combined: `4022` + `34` + `5` + `4320` → `40223454320`
  - Reversed: `02345432204`
  - Truncated to 8 chars: `02345432`
- **Output:** `02345432`
