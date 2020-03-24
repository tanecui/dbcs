import sqlite3
import traceback
from pprint import pprint
#from DBCSMap import load_dbcs_map
from DBCSMapping import loadMapping
from DBCSLogging import DBCSLogging
from getopt import getopt,GetoptError
import sys

bad_list = []

dbcs_map = loadMapping()
logging = DBCSLogging()
logger = logging.getLogger(loggerName='DBCS2Chinese_v2')

def process(input_file, output_file):
    with open(input_file) as fp:
        with open(output_file,mode="w",encoding='utf-8') as wfp:
            lines = fp.readlines()
            for index,line in enumerate(lines):
                try:
                    new_line = handle_line(line)
                    wfp.write(new_line)
                except Exception as ex:
                    logger.debug("Line {} Cause Error {}".format(index,ex))

def handle_line(line):
    prefix_cif = line[0:9]
    prefix_account = line[9:25]
    name = line[25:105]
    address_1 = line[105:185]
    address_2 = line[185:265]
    address_3 = line[265:345]
    address_4 = line[345:425]
    suffix = line[425:]

    chinese_name = handle_chinese(name)
    chinese_address_1 = handle_chinese(address_1)
    chinese_address_2 = handle_chinese(address_2)
    chinese_address_3 = handle_chinese(address_3)
    chinese_address_4 = handle_chinese(address_4)

    format_chinese_name = "{:30s}".format(chinese_name)
    format_chinese_address_1 = "{:35s}".format(chinese_address_1)
    format_chinese_address_2 = "{:35s}".format(chinese_address_2)
    format_chinese_address_3 = "{:35s}".format(chinese_address_3)
    format_chinese_address_4 = "{:35s}".format(chinese_address_4)

    new_array = []
    new_array.append(prefix_cif)
    new_array.append(prefix_account)
    new_array.append(format_chinese_name)
    new_array.append(format_chinese_address_1)
    new_array.append(format_chinese_address_2)
    new_array.append(format_chinese_address_3)
    new_array.append(format_chinese_address_4)
    new_array.append(suffix)

    new_line = ''.join(new_array)
    
    return new_line


def get_convered_chinese(host_char):
    if host_char.strip() == '':
        return ' '
    try:
        convered_char = dbcs_map[host_char]
    except KeyError:
        print("host code {} not found ".format(host_char))
        bad_list.append(host_char)
        convered_char = ''
    return convered_char

def handle_chinese(chinesestr):
    str_len = len(chinesestr.strip())
    n = 4
    if str_len%n != 0:
        raise Exception('Chinese String is not correct {}, len {}'.format(chinesestr,str_len))
    convered_name = ''
    str = chinesestr.strip()
    #one chinese occupied 4 letters
    chunks = [str[i:i+n] for i in range(0, len(str), n)]
    for char in chunks:
        convered_name = convered_name+get_convered_chinese(char)
    return convered_name
def usage():
    print("""
    python -file {} <options>
    short options
    -i <input file>
    -o <output file>
    long options 
    --input=<input file>
    --output=<input file>
    """.format(sys.argv[0]))

def main():
    #default value
    input_file = '19M938_address_code_51_fixed.txt'
    output_file = '19M938_address_code_out_fixed.txt'
    try:
        opts, args = getopt(sys.argv[1:],shortopts="i:o:",longopts=["input=","output="])
        for opt,val in opts:
            if opt == '-i':
               input_file = val
            elif opt == '-o':
                output_file = val
    except GetoptError as err:
        logger.error(err)
        logger.error("opts {} args {}".format(opts,args))
    if input_file == '' or output_file == '':
        usage()
        exit(1)
    logger.debug("Input file {}".format(input_file))
    logger.debug("Output file {}".format(output_file))
    process(input_file, output_file)
    logger.info("Data Conversion Done!")
    logger.info("===== Error List =====")
    new_list = set(bad_list)
    for item in new_list:
        logger.info(item)

# def health_check():
#     with open('19M938_address_code_out_fixed.txt',encoding='utf-8') as fp:
#         lines = fp.readlines()
#         for line in lines:
#             if len(line) != 277:
#                 print(len(line))

if __name__ == "__main__":
    main()
    #health_check()