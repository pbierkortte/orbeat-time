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
- Used 365.2425 days per year, which is the Gregorian calendar standard
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

0. Get Unix timestamp in milliseconds
1. Add Caesar epoch offset and Prime Meridian adjustment
2. Convert to fractional days since Caesar
3. Extract years via division by 365.2425
4. Calculate week and day within 8-day cycle
5. Extract fractional part for sub-day precision
6. Convert each component to octal
7. Concatenate, reverse, truncate to 8 chars

## Example

Here is a by-hand calculation using the Unix timestamp `1700000000000`:

- **Input Milliseconds:** `1700000000000`

- **Step 1: Adjust for Epoch and Timezone**
  - Start with the input timestamp: `1700000000000`
  - Add the Caesar epoch offset: `+ 63517996800000`
  - Add the Prime Meridian offset: `+ (-32400000)`
  - **Resulting Milliseconds:** `65217964400000`

- **Step 2: Convert to Days**
  - Divide by the number of milliseconds in a day: `65217964400000 / 86400000`
  - **Result in Days:** `754837.5509259259`

- **Step 3: Calculate Year, Week, and Day**
  - **Year:** `floor(754837.5509259259 / 365.2425)` = `2066`
  - **Day of Year:** `floor(754837.5509259259 % 365.2425)` = `255`
  - **Week of Year:** `floor(255 / 8)` = `31`
  - **Day of Week:** `floor(754837.5509259259) % 8` = `5`

- **Step 4: Calculate the Fractional Part**
  - Take the decimal part from Step 2: `0.5509259259`
  - Multiply by 8 to the power of 4: `0.5509259259 * 4096`
  - **Resulting Fraction:** `2256.500000...` (we take the floor: `2256`)

- **Step 5: Convert to Octal**
  - Year `2066` = `4022` in octal
  - Week `31` = `37` in octal
  - Day `5` = `5` in octal
  - Fraction `2256` = `4320` in octal

- **Step 6: Combine and Finalize**
  - Concatenate the octal values: `4022` + `37` + `5` + `4320` = `40223754320`
  - Reverse the string: `02345732204`
  - Truncate to the first 8 characters: `02345732`

- **Final Output:** `02345732`
