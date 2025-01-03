# Orbeat Time

## Summary

Orbeat is an octal time system. It gets its name from a combination of octal, orbit, and beat. This naming reflects the system's structure, which utilizes an octal (base-8) representation to measure time in a continuous, orbit-like cycle.

## Links
- Live Demo: https://www.patbierkortte.com/orbeat-time

## Background

Loosely inspired by Swatch Internet Time (.beat time), a decimal time system introduced in 1998 used on ICQ and in the game Phantasy Star Online to facilitate cross-continent gaming. It also draws inspiration from batch codes used in retail and manufacturing industries for date codes and competitive intelligence.

## Motivation

I created this project out of intellectual curiosity and as a practical tool. It was a stimulating exercise that allowed me to combine various concepts across multiple disciplines. I needed an efficient and cryptic timestamping method, like batch codes, to manage public-facing personal documents. I sought to devise an innovative way to balance precision with obscurity by crafting a compact yet noteworthy date time code, which would be meaningful to me while remaining ambiguous for others.

## Design Decisions

My design decisions include:

- Using little-endian ordering, which is more common in modern computing systems
- Adopting a base-8 (octal) number system to avoid rounding issues common in decimal systems
- Flooring the total days before calculating years to ensure accurate year representation
- Full-year was omitted in favor of brevity and due to space constraints
- Including two fractional year digits to provide a division of the year (~5.7 days)
- Avoiding timezones to simplify global time representation
- Using the Unix epoch for convenience and to avoid leap-second complications
- The precision is ~21 seconds roughly in the scale of seconds
- Used 365.25 days per year, which is the Julian calendar standard

## Format

A concatenated string consisting of:
- Days since Unix epoch formatted with specific digit counts and then reversed
- Years since Unix epoch formatted with specific digit counts and then reversed

## Implementation

The encoding process involves the following steps:

0. Calculate the Unix timestamp in milliseconds
1. Convert the milliseconds to fractional days since the Unix epoch
2. Floor the total days and then convert the milliseconds to fractional years since the Unix epoch
3. Transform both days to octal format, preserving the fractional parts
4. Transform both years to octal format, preserving the fractional parts
5. Format each part (days and years) with specific digit counts for whole and fractional parts
6. Combine the formatted years and days
7. Reverse the concatenated string to generate the Orbeat time

## Example

The encoding process:

- **Input:**
  - Unix timestamp in milliseconds (e.g., `1700000000000`)
- **Conversion:** 
  - Days: `1700000000000 / 86400000` ≈ `19675.925925925927` days
  - Years: `Math.floor(19675.925925925927) / 365.25` ≈ `53.86721423682409` years
- **Octal Formatting:** 
  - Days: `19675.925925925927` → octal ≈ `46333.7320`
  - Years: `53.86721423682409` → octal ≈ `65.67`
- **Formatting with Digit Counts:**
  - Days: `46333.7320` → `3` (whole) + `7320` (fraction) → `37320`
  - Years: `65.67` → `5` (whole) + `67` (fraction) → `567`
- **Concatenation and Reversal:**
  - Combined: Years + Days  → `56737320`
  - Reversed: `02373765`
- **Output:** `02373765`
