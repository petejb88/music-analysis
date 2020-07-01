# ---------- Convert notearray to dataframe ----------
# Author: Peter Bonventre
# Goal: Take in a josquin notearray (or more generally any notearray from a humdrum file) and product a dataframe with the same data

import pandas as pd
from io import StringIO

import argparse

parser = argparse.ArgumentParser(description="Convert a notearray into a clean df")
parser.add_argument('notearray_path', help="Path to notearray")

args = parser.parse_args()



# notearray:
# 

def clean_notearray(notearray_path):
    '''
    Note arrays from Josquin have headers which give important metadata for the file, but which are not needed for the analysis. 
    This function removes them. 

    args:
         notearray_path: location of notearray.txt
    output:
         lines: a list of lines to be read by pandas as a csv
    '''
    
    with open(notearray_path, "r") as notearray:
        lines = notearray.readlines()
        
        # find start line
        header_lines = [ii for ii,line in enumerate(lines) if line.count('!') != 0]
        start_line_num = min(set(range(len(lines)))-set(header_lines))
        start_line = lines[start_line_num]
        end_line_num = max(set(range(len(lines))) - set(header_lines))

        # clean file
        lines = lines[start_line_num : end_line_num+1]
    
        # clean start_line
        start_line = start_line.replace('%','')
        lines[0] = start_line
        del lines[1]

        # act as newfile
        cleaned_notearray = StringIO('\n'.join(lines))

        return cleaned_notearray
        





def main():
    cleaned_notearray = clean_notearray(args.notearray_path)
    df = pd.read_csv(cleaned_notearray, delimiter='\t')
    # find: number of voices, ... actually, this was significantly less work than I thought
    print(df.columns)

if __name__ == "__main__":
    main()
