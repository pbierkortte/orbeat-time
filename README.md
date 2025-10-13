# Orbeat

## Summary

Orbeat is an octal-based cryptic timestamping system. It gets its name from a combination of octal, orbit, and beat. This naming reflects the system's structure, which utilizes an octal (base-8) representation to measure time in a continuous, orbit-like cycle based on a rational underlying calendar foundation.

## Links
- Live Demo: https://www.patbierkortte.com/orbeat
- UCY Project: https://github.com/pbierkortte/UCY

## Background

Loosely inspired by Swatch Internet Time (.beat time), a decimal time system introduced in 1998 used on ICQ and in the game Phantasy Star Online to facilitate cross-continent gaming, and batch codes used in retail and manufacturing industries for date codes and competitive intelligence. The underlying system draws from proven historical precedents like the Roman 8-day nundinal market cycle and astronomical precision.

## Motivation

I created this project out of intellectual curiosity and as a practical tool. It was a stimulating exercise that allowed me to combine various concepts across multiple disciplines. I needed an efficient and cryptic timestamping method, like batch codes, to manage public-facing personal documents. I sought to devise an innovative way to balance precision with obscurity by crafting a compact yet noteworthy timestamp code based on rational principles, which would be meaningful to me while remaining ambiguous for others.

## Design Decisions

My design decisions include:

-   Nundinal Cycle: The proven **Roman 8-day** week structure is a practical foundation for the calendar's rhythm
-   Historical Certainty: The epoch is an indisputable **historical anchor** point to guarantee absolute certainty
-   Scientific Precision: The epoch time is fixed with **scientific precision** for an unambiguous temporal reference
-   Astronomical Accuracy: The **Mean Tropical Year** of ~365.2422 days prevents seasonal drift and ensures ~200 year accuracy
-   Octal Encoding: Dates use **octal encoding** for mathematical harmony and to require explanation to decode
-   Cryptic Output: The output is made cryptic via **reversal and truncation** to 8 characters for a compact code
-   Spring Equinox: The years **align with spring equinox** for practical synchronization for the foreseeable future
-   Generational Stability: Pattern runs are **~27 years long** providing consistent calendar behavior across generations
-   Week Zero: The first week **hides** in short years to maintain year-end alignment

## Format

**Reversed:**
`digit_of_year` `week_of_year` `day_of_week` `fraction_of_day`

A concatenated string consisting of:
- Years since Epoch formatted in octal
- Weeks within the year formatted in octal (2 digits)
- Days within the 8-day week formatted in octal
- Fractional day component formatted in octal (4 digits)
- The concatenated string is then reversed and truncated to 8 characters
