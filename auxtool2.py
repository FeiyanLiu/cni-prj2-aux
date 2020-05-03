import os
from os.path import join, getsize
from sys import argv

def calc_size(path_src, result):
    with open(result, 'w', encoding="utf-8") as f:
        calc_size_inner(path_src, f)

def calc_size_inner(path_src, file_stream):
    for root, dirs, files in os.walk(path_src):
        for file in files:
            print("%40d"%getsize(join(root,file)),"*",end="",file=file_stream)
            print(".",end="",file=file_stream)
            print(root[len(path_src):].replace("\\","/"),end="/",file=file_stream)
            print(file,file=file_stream)

def compare_files(num, detail_file):
    print()
    print("Source Path", "Total Size (B)", "Correct", "Wrong", "Fabricate", "Lost", sep="\t")
    print("===========", "==============", "=======", "=====", "=========", "====", sep="\t")
    with open(detail_file, 'w') as f:
        for i in range(1,num+1):
            path_src="src%d.sha1"%i
            path_dst="dst%d.sha1"%i
            path_size="size%d.txt"%i
            compare_hash(path_src, path_dst, path_size, f)


def compare_hash(path_src, path_dst, path_size, file_stream):
    fs_dst = open(path_dst, encoding="utf-8").readlines()
    fs_src = open(path_src, encoding="utf-8").readlines()
    fs_size = open(path_size, encoding="utf-8").readlines()
    map_dst = {}
    map_src = {}
    map_size = {}
    for line in fs_dst:
        map_dst[line[42:-1]] = line[:40]
    for line in fs_src:
        map_src[line[42:-1]] = line[:40]
    for line in fs_size:
        map_size[line[42:-1]] = int(line[:40])

    map_fabricate = [i for i in map_dst if i not in map_src]
    map_lost = [i for i in map_src if i not in map_dst]
    map_right = [i for i in map_src if i in map_dst and map_src[i]==map_dst[i]]
    map_wrong = [i for i in map_src if i in map_dst and map_src[i]!=map_dst[i]]

    print("======", path_src, "vs.", path_dst, "======", file=file_stream)
    print("Fabricated files:", file=file_stream)
    for i in map_fabricate:
        print(i, map_dst[i], file=file_stream)
    print("Lost files:", file=file_stream)
    for i in map_lost:
        print(i, map_src[i], file=file_stream)
    print("Wrong files:", file=file_stream)
    for i in map_wrong:
        print(i, map_src[i], file=file_stream)
    print("Correct files:", file=file_stream)
    total_size = 0;
    for i in map_right:
        print(i, map_src[i], file=file_stream)
        total_size += map_size[i]

    print("%-11s"%path_src[:11], "%13d"%total_size, "%7d"%len(map_right), "%5d"%len(map_wrong), "%8d"%len(map_fabricate), "%4d"%len(map_lost), sep="\t")

def print_title():
    print("Auxiliary Tool of Project 2 (Version 1.0)")
    print("Author: Dr. Wei HUANG, School of Informatics, Xiamen University")
    print("        Shengsen WU, School of Electronic and Computer Engineering, Peking University")

def usage():
    print("")
    print("Usage: python auxtool2.py --[opt] [args]")
    print("    * opt     : Options. It should start with \"--\" and it can be \"help\", \"size\", \"compare\".")
    print("        - help     : See this usage. By default.")
    print("        - size     : Output the sizes of all files in the directory to the destination file.")
    print("        - compare  : Compare source and destination SHA1 files, and output the summary and detail results.")
    print("    * args     : Arguments. It depends on [opt].")
    print("        - Usage 1: python auxtool2.py --help")
    print("            > No arguments.")
    print("        - Usage 2: python auxtool2.py --size [dir] [result]")
    print("            > dir     : The directory to get file sizes.")
    print("            > result  : The destination file to save the result.")
    print("        - Usage 3: python auxtool2.py --compare [num] [detail]")
    print("            > num     : Number of repetitions.")
    print("            > detail  : The file to log the detail result.")
    print("")
    print("Please follow the following instructions:")
    print("    1. Run Linux command")
    print("          \"find . -type f -print0 | xargs -0 sha1sum > ./src1.sha1\" ")
    print("       in the source directory, and run Linux command ")
    print("          \"find . -type f -print0 | xargs -0 sha1sum > ./dst1.sha1\" ")
    print("       in the destination (remote) directory;")
    print("    2. Run this tool to get the sizes of all the files of source directory using command")
    print("          \"python auxtool2.py --size src size1.txt\";")
    print("    3. Repeat Steps 1 and 2 for several times.")
    print("    4. Run this tool using command")
    print("          \"python auxtool2.py --compare 5 detail.txt\".")

def main():
    print_title()
    try:
        if len(argv) == 3 or argv[1] == "--size":
            calc_size(argv[2], argv[3])
        elif len(argv) == 3 or argv[1] == "--compare":
            compare_files(int(argv[2]), argv[3])
        else:
            usage()
            raise ValueError("Wrong command line format.")
    except Exception as e:
        print(e)
        exit()

if __name__ == "__main__":
    main()
