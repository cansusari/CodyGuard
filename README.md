# CodyGuard

Codyguard is a LookML linter tool that makes static code analysis using Python.

In this repo:
- CodyGuard file includes the functions that are used to analyze the LookML scripts, and the main file assures the integration within the instance, triggered by each commit in an open merge request.
- The structure consists of two classes, one of which is the CodyGuard itself, and the other is CodyGuardFunc where we have the generic functions that will be used inside the CodyGuard.
- lkml library is used for parsing, but in some cases analysis are made directly from raw text.
- All functions are connected to one main function, check_file(), and the dependency of the functions are hierarchical.
- Depending on the file's type, the function calls the check_view() or check_explore() functions, and they call the necessary ones.
- The results from the functions are kept in a val_result string object and the errors and warnings are grouped and shown under the corresponding titles.

For detailed information, you can check the medium article: https://medium.com/@dataguards/6584e14293b
