BEGIN {
FS="\t"
}
{
printf($2 "%%%\t%%%")
getline
#printf($2 "%%%\t%%%")
#getline 
printf($2 "%%%\t\n")
}
