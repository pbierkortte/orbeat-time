# Orbeat Time

## Summary

Orbeat is an octal time system. It gets its name from a combination of octal, orbit, and beat. This naming reflects the system's structure, which utilizes an octal (base-8) representation to measure time in a continuous, orbit-like cycle.

## Background

Loosely inspired by Swatch Internet Time (.beat time), a decimal time system introduced in 1998 used on ICQ and in the game Phantasy Star Online to facilitate cross-continent gaming. It also draws inspiration from batch codes used in retail and manufacturing industries for date codes and competitive intelligence.

## Motivation

I created this project out of intellectual curiosity and as a practical tool. It was a stimulating exercise that allowed me to combine various concepts across multiple disciplines. I needed an efficient and cryptic timestamping method, like batch codes, to manage public-facing personal documents. I sought to devise an innovative way to balance precision with obscurity by crafting a compact yet noteworthy date time code, which would be meaningful to me while remaining ambiguous for others.


## Design Decisions

My design decisions include:

- Using little-endian ordering, which is more common in modern computing systems
- Adopting a base-8 (octal) number system to avoid rounding issues common in decimal systems
- Full-year was omitted in favor of brevity and due to space constraints
- Avoiding timezones to simplify global time representation
- Using the Unix epoch for convenience and to avoid leap-second complications
- The precision is ~21 seconds roughly in the scale of seconds

## Format

An 8-character string, where:

- The first four digits are from the fractional part of octal days (reversed)
- Digits 5-7 are extracted from the integer part of octal days (reversed)
- The 8th digit is the last digit of the current year


## Implementation

Steps:

0. Fetch the current time
1. Calculate the Unix timestamp in milliseconds
2. Calculate years since 1970 modulo 8
3. Convert the timestamp to fractional days since the Unix epoch
4. Transform fractional days to octal format, preserving the fractional part
5. Extract specific digits from the octal representation
6. Combine these elements with the last digit of the years
7. Reverse the sequence to get the Orbeat time
