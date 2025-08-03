Data Cleaning and Standardization

Whitespace and Punctuation: Standardized formatting by correcting misplaced punctuation and handling multiple whitespaces.

Unicode to ASCII: Converted all Unicode characters to standard ASCII to ensure compatibility and consistency.

Middle Initial Detection: Developed a methodology to accurately identify and correct middle initials that lacked a space or punctuation.

Performance Optimization
Due to performance issues with numpy.unique() on a 32-million-value dataset, an efficient workaround was implemented. The dataset was sliced and processed alphabetically by the first letter of each full name. The cleaned data was then written to a new alphabetized flat-text file.

Supplemental Datasets Created

Diminutives: Created comprehensive lists of male and female diminutives by scraping Wikipedia and various search engines.

Business Names: Compiled a dataset of 1.7 million active business names from the Oregon and Washington Secretary of State OpenData Portals.

Transliterations: Created a dataset of US/English name transliterations across all known languages.

Abbreviations: Compiled a dataset of company abbreviations and initialisms from around the world.

Honorifics and Suffixes: Created a dataset of all known honorifics, prefixes, and titular suffixes.
