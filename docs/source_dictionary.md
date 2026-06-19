# Week 7 Dataset Package — Source Dictionary

## locations.csv
Reference table for the fixed set of teaching locations used in the weather API calls.

Columns:
- location_id: short location code used as the business key
- city: city name
- country_code: ISO 3166-1 alpha-2 country code
- country_name: country name
- latitude / longitude: coordinates for API calls
- region: teaching region grouping
- climate_zone: simplified climate category

## date_dimension.csv
Prepared date dimension for May 2024.

## country_indicators.csv
Teacher-prepared annual country indicator snapshot for selected countries.

## weather_good_sample.csv
Backup/generated weather file for classroom use if the API is unavailable.

## weather_corrections_bad.csv
Deliberately corrupted version of the good weather file for validation and recovery labs.
