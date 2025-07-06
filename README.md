# Orbeat Time

## Summary

Orbeat is an octal-based cryptic timestamping system. It gets its name from a combination of octal, orbit, and beat. This naming reflects the system's structure, which utilizes an octal (base-8) representation to measure time in a continuous, orbit-like cycle based on a rational underlying calendar foundation.

## Links
- Live Demo: https://www.patbierkortte.com/orbeat-time

## Background

Loosely inspired by Swatch Internet Time (.beat time), a decimal time system introduced in 1998 used on ICQ and in the game Phantasy Star Online to facilitate cross-continent gaming, and batch codes used in retail and manufacturing industries for date codes and competitive intelligence. The underlying system draws from proven historical precedents like the Roman 8-day nundinal market cycle and astronomical precision.

## Motivation

I created this project out of intellectual curiosity and as a practical tool. It was a stimulating exercise that allowed me to combine various concepts across multiple disciplines. I needed an efficient and cryptic timestamping method, like batch codes, to manage public-facing personal documents. I sought to devise an innovative way to balance precision with obscurity by crafting a compact yet noteworthy timestamp code based on rational principles, which would be meaningful to me while remaining ambiguous for others.

## Design Decisions

My design decisions include:

-   **Spring Equinox Foundation:** The year begins on the **Spring Equinox** for practical alignment with natural cycles
-   **8-day Nundinal Cycle:** The **proven Roman 8-day week structure** is a practical foundation for the calendar's rhythm
-   **Historical Certainty Epoch:** The epoch is an **indisputable historical anchor point** to guarantee absolute certainty
-   **Scientific Precision:** The epoch time is fixed with **scientific precision** for an unambiguous temporal reference
-   **Astronomical Accuracy:** The **Mean Tropical Year of 365.24219 days prevents seasonal drift** and ensures perpetual accuracy
-   **Octal Encoding:** Dates use **octal encoding** for mathematical harmony and to **require explanation to decode**
-   **Cryptic Output:** The output is made **cryptic** via **reversal and truncation to 8 characters** for a compact code

## Format

A concatenated string consisting of:
- Years since Epoch formatted in octal
- Weeks within the year formatted in octal (2 digits)
- Days within the 8-day week formatted in octal
- Fractional day component formatted in octal (4 digits)
- The concatenated string is then reversed and truncated to 8 characters

## Implementation

The encoding process involves the following steps:

0. Convert input timestamp to fractional days since Epoch (March 21, 44 BCE at 09:00 UTC)
1. Calculate the **Year** (`year_int`) and **Day of the 8-day Week** (`day_int`) from the total day count
2. Calculate the **Day of the Year** (`day_in_year`) using the Mean Tropical Year length (365.24219 days)
3. Calculate the **Week of the Year** (`week_int`) by aligning the `day_in_year` with the 8-day cycle
4. Extract the **Fractional Part** of the day for sub-day precision
5. Convert all calculated components (Year, Week, Day, Fraction) to their formatted octal string representations
6. Concatenate the octal strings in order, reverse the resulting string, and truncate to 8 characters
7. Output the final 8-character cryptic timestamp

## Example

- **Input Milliseconds:** `1700000000000`

- **Step 1: Adjust for Epoch**
  - Start with the input timestamp: `1700000000000`
  - Convert to days since March 21, 44 BCE at 09:00 UTC
  - **Resulting Days Since Epoch:** `755179.509722`

- **Step 2: Calculate Time Components**
  - **Year:** Total days divided by Mean Tropical Year: `755179.509722 / 365.24219 = 2067.956`
  - **Year Integer:** `2067`
  - **Day of Year:** Remainder from year calculation: `349`
  - **Day of Week:** Total days modulo 8: `755179 % 8 = 3`
  - **Week of Year:** `(349 - 3) / 8 = 43`
  - **Fractional Part:** `0.509722 × 4096 = 2087`

- **Step 3: Convert to Octal**
  - Year `2067` = `4023`
  - Week `43` = `53`
  - Day `3` = `3`
  - Fraction `2087` = `4047`

- **Step 4: Combine and Finalize**
  - Concatenate the octal values: `4023` + `53` + `3` + `4047` = `402353340447`
  - Reverse the string: `744043535204`
  - Truncate to the first 8 characters: `74404353`

- **Final Output:** `74404353`
