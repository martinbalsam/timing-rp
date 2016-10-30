import re
import argparse
"""
This script sanitize the raw data experted from "Timing.app",
it adds the proper double quotes around the "Path" attribute,
and it removes unwanted double quotes inside the "Path" attribute,
that may yield an unwanted escape of the field.

--- TODO ---
speedup:
as for now I'm iterating twice over the whole list,
Maybe the sanitizing can be done in a single regex, but I spent waay to much time
coming up with these. I'll leave it to somebody else (noone)


cleanup:
delete unused files
"""
parser = argparse.ArgumentParser(description="writes the input data into a sanitized .csv file")
parser.add_argument('path', nargs=1, type = str, help='the path of the input raw .csv file to parse')
args = parser.parse_args()


"""paths of the input and output data
   each file has the same name structure:
   file.csv
   file_tmp_.csv
   file_san_.csv  (THIS IS THE OUTPUT WE WANT, SANITIZED AND SHIT)
   file_err_.log
"""
input_data = args.path[0]
temp_data = args.path[0][:-4]+"_tmp_.csv"
output_data = args.path[0][:-4]+"_san_.csv"
errors_log = args.path[0][:-4]+"_err_.log"


#THIS SHIT WORKS IF THERE ARE NO UNEXPECTED BREAKLINE
errors = open(errors_log,'w')
with open(input_data,'r') as original:
    with open(temp_data,'w') as new:
        #writes the csv header
        new.write(original.readline())
        for line in original:
            #regex to isolate the 'path' attribute
            matches = re.search('(^[^,]+,)(.*)(,\d{2}/\d{2}/\d{2} \d{2}:\d{2},\d{2}/\d{2}/\d{2} \d{2}:\d{2},.*$)', line)
            try:
                #add quotation around the path attribute and writes it in a new file
                new.write(matches.group(1)+'"'+matches.group(2)+'"'+matches.group(3)+'\n')
            #catches lines that don't match the regex and writes them in an errors.log file
            except AttributeError:
                errors.write(line)
                continue

#Now I recheck the whole list to catch if there are extra double quotation signs (") in the path attribute,
#if so, we delete them


with open(temp_data,'r') as old:
    with open(output_data,'w') as new:
        new.write(old.readline())
        for line in old:
            #regex that catches any path that contains one or more double quotation sign (")
            matches = re.search('(^[^,]+,")(.*".*)(",\d{2}/\d{2}/\d{2} \d{2}:\d{2},\d{2}/\d{2}/\d{2} \d{2}:\d{2},.*$)', line)
            if matches is not None:
                #deletes any double quotation mark (") and writes tha sanitized line in a new file
                new.write(matches.group(1)+matches.group(2).replace('"','')+matches.group(3)+'\n')
            #if the line is ok, it just writes the line in the new file
            else:
                new.write(line)

#populate a panda DataFrame object with the data, and the proper datetime objects
"""dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%y %H:%M')
a = pd.read_csv('bin/fine.csv', parse_dates=[2,3], date_parser=dateparse)
"""
