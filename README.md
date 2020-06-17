# remove-stale-macros

## RemoveStaleMacros is a utility which helps in refactoring stale/dead macros from your code. It automatically removes the supplied macros with no manual intervention. It can handle all the nested macros :)

Usage:
-----

1. Clone or download the file: RemoveStaleMacros.py
2. Run: `python RemoveStaleMacros.py [give_full_directory_or_file_path] [list_of_macros_to_remove]`

For example: `python RemoveStaleMacros.py /Users/strike/Desktop/testfiles MACRO_X MACRO_Y MACRO_Z`

Sample output:
-------------
Suppose the input file is something like: 
```
#ifdef MACRO_X
	line 1
	line 2
#ifdef MACRO_Y		
	line 3
	line 4
#endif
	line 5
	line 6
#else
	line 7
	line 8
#endif
```
If you run the utility to remove MACRO_X, the output file will look like:
```
	line 1
	line 2
#ifdef MACRO_Y		
	line 3
	line 4
#endif
	line 5
	line 6
```

Notes:
----
* This is an initial draft which means it's a naive implementation, which can certainly be optimized a lot.

* Files need to have write permission first before the utility can edit those files.

* After removal of stale macros, files might not end up properly indented but that is something which IDEs can automatically indent.


