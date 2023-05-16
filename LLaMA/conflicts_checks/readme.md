	Cloned the github "Names Dataset" of leaked/scraped Facebook Names (491M)
	Cleaned the "US Names" dataset of 32M names
	Methodology for detecting Middle Initials without a space or punctuation and enacting corrections thereon
	Conversion to lowercase, Whitespaces, Odd/Misplaced Punctuation
	Cleaned out Unicode characters to standard ASCII
	Numpy.Unique() method did NOT like 32M values to be handled simultaneously
o	Iterated over slicing a Pandas DataFrame by the first value of a Full Name by using for I in range(0,25):  then slicing the values by evaluating if [:1] is chr(97+i) Then used the writelines() method to append to a new alphabetized flat-text file
	Created a dataset for all Male Diminutives by scraping Wikipedia and bing/google searches
	Created a dataset for all Female Diminutives by scraping Wikipedia and bing/google searches
	Created a dataset for 1.7M Active Business Names from the Oregon and Washington Secretary of State OpenData Portal datasets
	Created a dataset for all US/English Name transliterations all known languages
	Created a dataset for all Company Abbreviations/Initialisms in the world
	Created a dataset for all Honorifics, Prefixes, and all titular Suffixes.
