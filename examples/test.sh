#! /bin/sh
set -e

t1=t1.pdf
t2=t2.pdf
output=output.pdf
python ../recombine.py $t1 $t2 1-$output "1#1,2#0"
python ../recombine.py $t1 $t2 2-$output "1#1,2#0,1#1"
python ../recombine.py $t1 $t2 3-$output "1#1,2#0,1#1=r90"
python ../recombine.py $t1 $t2 4-$output "1#0:10=r-90,2#12:15=r90,1#0"
python ../recombine.py $t1 $t2 5-$output "1#0:10=r180,2#12:15=r90,1#0"
