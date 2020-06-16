import re
import argparse
import os

ifdef_macro_pattern = r'.*(#ifdef|#if) (\w+)'
ifndef_macro_pattern = r'.*#ifndef (\w+)'
endif_macro_pattern = r'.*(#endif)'
else_macro_pattern = r'.*(#else)'

def process_file(file, stale_macros):
     f = open(file, 'r+')

     processing_macros = []
     processed_lines = []

     lines = f.readlines()
     i = 0
     while i < len(lines):
         current_line = lines[i]
         # push this current_line
         processed_lines.append(current_line)

         # patterns
         matched_ifdef_macro = re.match(ifdef_macro_pattern, current_line)
         matched_ifndef_macro = re.match(ifndef_macro_pattern, current_line)
         matched_endif = re.match(endif_macro_pattern, current_line)
         matched_else = re.match(else_macro_pattern, current_line)

         if matched_ifdef_macro is not None:
             # we found an ifdef statement, True signifies that
             macro = matched_ifdef_macro.group(2)
             processing_macros.append((macro, True, len(processed_lines) - 1))

         elif matched_ifndef_macro is not None:
             # we found an ifndef statement, False signifies that
             macro = matched_ifndef_macro.group(1)
             processing_macros.append((macro, False, len(processed_lines) - 1))

         elif matched_endif is not None:
             # we found an endif statement
             if len(processing_macros) is 0:
                 print(current_line, i)
                 raise Exception('Expected processing_macros stack not to be empty')

             current_macro, is_ifdef, index = processing_macros.pop()
             if current_macro in stale_macros:
                 if is_ifdef:
                     # here we remove the ifdef and endif line and keep the lines which were in between
                     processed_lines = processed_lines[:index] + processed_lines[index + 1: len(processed_lines) - 1]
                 else:
                     # here we remove the ifndef and endif line and also the lines which were in between
                     processed_lines = processed_lines[:index]

         elif matched_else is not None:
             # we found an else statement
             # current top element
             if len(processing_macros) is 0:
                 print(current_line, i)
                 raise Exception('Expected processing_macros stack not to be empty')

             top_macro, is_ifdef, index = processing_macros[-1]
             if top_macro in stale_macros:
                 # pop the '#else' which we would have pushed
                 processed_lines.pop()
                 # insert an endif to match currently prcoessing macro
                 lines.insert(i + 1, '#endif\n')
                 # now to take care of else part, push another ifndef/ifdef macro
                 if is_ifdef:
                     lines.insert(i + 2, '#ifndef ' + top_macro + '\n')
                 else:
                     lines.insert(i + 2, '#ifdef ' + top_macro + '\n')

         i += 1

     f.seek(0)
     f.write(''.join(processed_lines))
     f.truncate()


def process_files(path, stale_macros):
    for root, dirs, files in os.walk(path):
        for file in files:
            process_file(os.path.abspath(path) + '/' + file, stale_macros)
        for directory in dirs:
            process_files(os.path.abspath(directory), stale_macros)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Strip away stale macros from your C/C++ files')
    parser.add_argument('path', help='directory or file path to parse')
    parser.add_argument('strip_these_macros', nargs='+', help='list of macro names to strip away')
    args = parser.parse_args()

    process_files(args.path, args.strip_these_macros)