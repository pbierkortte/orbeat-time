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

- Using Caesar's death as the Datum (March 15, 44 BCE) for historical certainty and spring alignment
- Using little-endian ordering, which is more common in modern computing systems
- Adopting a base-8 (octal) number system to avoid rounding issues common in decimal to floating-point arithmetic
- Week increments on day rollover or year-end for consistency
- 8-day week structure following the Roman nundinal market cycle
- Fixed Eastern timezone Dawn adjustment for natural day boundaries
- The precision is ~21 seconds roughly in the scale of seconds
- Used 365.2425 days per year, which is the Gregorian calendar standard
- Reversal and truncation to 8 characters for cryptic output

## Format

A concatenated string consisting of:
- Years since Datum formatted in octal
- Weeks within the year formatted in octal (2 digits)
- Days within the 8-day week formatted in octal
- Fractional day component formatted in octal (4 digits)
- The concatenated string is then reversed and truncated to 8 characters

## Implementation

The encoding process involves the following steps:

0. Convert Unix timestamp to fractional days since Datum (with timezone adjustment)
1. Calculate the **Year** (`year_int`) and **Day of the 8-day Week** (`day_int`) from the total day count
2. Calculate the **Day of the Year** (`day_in_year`), which is the day count within the current Orbeat year
3. Calculate the **Week of the Year** (`week_int`) by aligning the `day_in_year` with the `day_int`
4. Extract the **Fractional Part** of the day for sub-day precision
5. Convert all calculated components (Year, Week, Day, Fraction) to their formatted octal string representations
6. Concatenate the octal strings in order, reverse the resulting string, and truncate to 8 characters
7. Output the final 8-character string

## Example

- **Input Milliseconds:** `1700000000000`

- **Step 1: Adjust for Epoch and Timezone**
  - Start with the input timestamp: `1700000000000`
  - Add the Datum offset: `+ 63517996800000`
  - Add the Dawn offset: `+ (-32400000)`
  - **Resulting Milliseconds:** `65217964400000`

- **Step 2: Convert to Days**
  - Divide by the number of milliseconds in a day: `65217964400000 / 86400000`
  - **Result in Days (`days_since`):** `754837.550925926`
  - **Integer part (`days`):** `754837`

- **Step 3: Calculate Time Components**
  - **Year:** To find the number of years, we take the whole number part of the total days divided by the number of days in a year: `754837 / 365.2425` gives us `2066`
  - **Day of Year:** The day of the year is the remainder of the same division, which is `245`
  - **Day of Week:** The day of the week is the remainder when the total days are divided by 8: `754837 / 8` leaves a remainder of `5`
  - **Week of Year:** To find the week of the year, we subtract the day of the week from the day of the year and divide by 8: `(245 - 5) / 8` gives us `30`
  - **Fractional Part:** To get the fractional part of the day, we multiply the decimal part of the `days_since` value by 8 to the power of 4 (4096): `0.550925926 * 4096` gives us `2256`

- **Step 4: Convert to Octal**
  - Year `2066` = `4022`
  - Week `30` = `36`
  - Day `5` = `5`
  - Fraction `2256` = `4320`

- **Step 5: Combine and Finalize**
  - Concatenate the octal values: `4022` + `36` + `5` + `4320` = `40223654320`
  - Reverse the string: `02345632204`
  - Truncate to the first 8 characters: `02345632`

- **Final Output:** `02345632`
