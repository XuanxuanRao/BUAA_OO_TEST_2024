set starttime=%time%

type %1 | java -jar %2 > %3

set endtime=%time%
echo %starttime%
echo %endtime%
