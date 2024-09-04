# Orbeat Time

## Summary

Orbeat is a octal time system. It gets its name from a combination of octal, orbit, and beat. This naming reflects the system's structure, which utilizes an octal (base-8) representation to measure time in a continuous, orbit-like cycle. 

## Background

Loosely inspired by Swatch Internet Time (.beat time), a decimal time system introduced in 1998. Swatch Internet Time was used as a reference on ICQ and in the online game Phantasy Star Online to facilitate cross-continent gaming.

## Design Decisions

Key design decisions include:

- Using little-endian ordering, which is more common in modern computing systems
- Adopting a base-8 (octal) number system to avoid rounding issues common in decimal systems
- Full year was omitted in favor of brevity and due to space constraints
- Avoiding timezones to simplify global time representation
- Using the Unix epoch for convenience and to avoid leap second complications
- The precision ~21 seconds roughly in the scale of seconds

## Format

An 8-character string, where:

- The first 4 digits are from the fractional part of octal days (reversed)
- Digits 5-7 are extracted from the integer part of octal days (reversed)
- The 8th digit is the last digit of the current year


## Implementation

Steps:

0. Fetch the current time
1. Calculate the Unix timestamp in milliseconds
2. Determine the year
3. Convert the timestamp to fractional days since the Unix epoch
4. Transform fractional days to octal format, preserving the fractional part
5. Extract specific digits from the octal representation
6. Combine these elements with the last digit of the current year
7. Reverse the sequence to get the Orbeat time
