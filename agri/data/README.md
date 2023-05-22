# Using Reconcile

To start the reconciliation server download the latest jar file from (here)[http://okfnlabs.org/reconcile-csv/], then start it with:

```shell
java -Xmx2g -jar reconcile-csv-0.1.2.jar <CSV-File> <Search Column> <ID Column>
```

CSV-File is the csv file you will use as a basis of reconciliation. As stated above preferably the cleaner, more complete or trusted one. You will introduce the unique IDs from that file to the other file.

Search Column is the primary column you want to use for matching. E.g. you want to match facilities with names spelled slightly differently - this would be the column to add here.

ID Column is the column containing unique ids for the facilities - if you don’t have one: generate one.
