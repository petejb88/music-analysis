# ---------- Convert notearray to dataframe ----------
# Author: Peter Bonventre
# Goal: Take in a josquin notearray (or more generally any notearray from a humdrum file) and product a dataframe with the same data


import pandas as pd
import torch
import torch.nn as nn
import re

from io import StringIO



# ---------- input arguments ----------
import argparse

parser = argparse.ArgumentParser(description="Convert a notearray into a clean df")
parser.add_argument('notearray_path', help="Path to notearray")

args = parser.parse_args()



# import data
class NoteArray(torch.utils.data.Dataset):
    '''
    All the info about the note array
    '''
    
    def __init__(self,notearray_path):
        """
        initialize: convert to df and metadata
        """

        with open(notearray_path, "r") as notearray:
            """
            self.lines = whole notearray, line-by-line
            self.notelines = the music part of the notearray
            self.notelines_totals = the totals of each column
            self.df, self.df_totals = df-ization of the above lines (columns = voices+, rows = time)
            self.composer, self.title, self.genre = composer, title, genre
            self.num_voices = number of voices (int)
            """
            
            self.lines = notearray.readlines()
            self.meta_lines = {
                ii:line for ii,line in enumerate(self.lines) if line.count('!') != 0
            }
            start_line_num = min(set(range(len(self.lines)))-set(list(self.meta_lines.keys())))
            end_line_num = max(set(range(len(self.lines))) - set(list(self.meta_lines.keys())))
            notelines =  self.lines[start_line_num : end_line_num+1]
            start_line = notelines[0]
            notelines[0] = start_line.replace('%','')
            
            # totals
            notelines_totals = notelines[:2]
            
            # just the music itself
            del notelines[1]
            self.notelines = notelines
            
            cleaned_notearray = StringIO('\n'.join(self.notelines))
            cleaned_totals = StringIO('\n'.join(notelines_totals))
            
            self.df = pd.read_csv(cleaned_notearray, delimiter='\t')
            self.df_totals = pd.read_csv(cleaned_totals, delimiter='\t')
            
            # metadata
            meta_dic = {}
            for line in list(self.meta_lines.values()):
                try: # not all meta lines are tab separated, but the ones we need are
                    a,b = re.split(r'\t+', line.rstrip('\n'))
                    meta_dic[a] = b
                except:
                    continue

            # self.meta_dic = meta_dic

            self.composer = meta_dic['% !!!COM:']
            self.title = meta_dic['% !!!OTL:']
                        
            try:
                self.num_voices = int(meta_dic['% !!!voices:'])
            except:
                self.num_voices = int(meta_dic['% !!!voices-ORP:'])
                
            try:
                self.genre = meta_dic['% !!!AGN:']
            except:
                self.genre = None
                










































def main():
    cleaned_notearray = clean_notearray(args.notearray_path)
    df = pd.read_csv(cleaned_notearray, delimiter='\t')
    # find: number of voices, ... actually, this was significantly less work than I thought
    print(df.columns)

if __name__ == "__main__":
    main()





# ---------- OLD PROGRAMMING ---------- 
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
        





