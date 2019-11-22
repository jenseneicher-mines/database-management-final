# Change names like "Brewhouse, The" to " The Brewhouse" and remove all double quotes
sed -e 's/\(\"[^",]\+\),\([^",]*\)/\2 \1/g' -e 's/\"//g' beer_reviews.csv > test.csv
# Change those names to The Brewhouse <- no stupid space at the beginning
sed 's/, /,/g' test.csv > test1.csv
# Remove the time field
cut -d, -f3 --complement test1.csv > test2.csv
# remove lines that haven't complied thus far
awk -F',' 'NF==12' test2.csv > test3.csv
# Put this back in the og file and remove temporay files
mv test3.csv beer_reviews.csv
rm test.csv
rm test1.csv
rm test2.csv
