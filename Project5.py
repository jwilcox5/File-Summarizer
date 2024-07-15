# Program By: Jack Wilcox

import os
import shutil
import re
import subprocess
import tarfile


def print_list(target_list):
    result = ''
    for val in target_list:
        result += val + '<br>'

    return result


def create_html_index_file():
    f = open('index.html', 'w')

    index_html_template = f"""<html> 
            <head> 
            <title>index.html</title> 
            </head> 
            <body> 
            <h1>Jack Wilcox's CSC 344 Projects</h1>
            <h2>
            <a href={'summary_a1.html'}>Project 1 (C)</a>
            </h2> 
            <h3>This project simulates a Turing Machine in C</h3>
            <h2>
            <a href={'summary_a2.html'}>Project 2 (Clojure)</a>
            </h2>
            <h3>This project implements a propositional logic inference system in Clojure</h3>
            <h2>
            <a href={'summary_a3.html'}>Project 3 (OCaml)</a>
            </h2>
            <h3>This project implements a recursive descent parser that performs pattern matching on strings in OCaml</h3>
            <h2>
            <a href={'summary_a4.html'}>Project 4 (Answer Set Programming)</a>
            </h2>
            <h3>This project creates a path finding algorithm for a social distancing scenario in Answer Set Programming</h3>
            <h2>
            <a href={'summary_a5.html'}>Project 5 (Python)</a>
            </h2>
            <h3>This project collects all of the previous programs (Including this one), summarizes them, and then emails it to a recipient</h3>
            </body> 
            </html> 
            """

    f.write(index_html_template)
    f.close()

    return 'index.html'


def create_html_summary_file(target_file, index_count):
    cur_parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    os.chdir(cur_parent_directory)

    source = os.getcwd() + '/a' + str(index_count) + '/' + target_file
    dest = os.getcwd() + '/' + target_file

    shutil.copyfile(source, dest)

    html_file_name = 'summary_a' + str(index_count) + '.html'

    f = open(html_file_name, 'w')

    proc = subprocess.check_output(['wc', '-l', target_file])
    out = str(proc)

    space_index = out.find(' ')

    file_name = out[space_index + 1:-3]
    file_line_count = out[2:space_index]

    classes = list()
    functions = list()
    variables = list()

    ############################################# C Program #############################################

    if file_name.endswith('.c'):
        c_class_ptrn = re.compile(r'struct\s+(\w+)')
        c_func_ptrn = re.compile(r'void\s+(\w+)\(')
        c_var_ptrn = re.compile(r'(\w+(\[\d+])?)\s*=\s*.*')

        file = open(file_name, 'r')
        lines = file.readlines()

        for line in lines:
            if not line.__contains__('//'):
                c_class_match = c_class_ptrn.search(line)
                if c_class_match:
                    if not classes.__contains__(c_class_match.group(1)):
                        classes.append(c_class_match.group(1))

                c_func_match = c_func_ptrn.search(line)
                if c_func_match:
                    if not functions.__contains__(c_func_match.group(1)):
                        functions.append(c_func_match.group(1))

                c_var_match = c_var_ptrn.search(line)
                if c_var_match:
                    c_var_string = str(c_var_match)
                    apost_index = c_var_string.find('\'')
                    regex_result = c_var_string[apost_index + 1:-2]

                    if regex_result.__contains__('[') and line.__contains__('char'):
                        var_bracket_index = regex_result.find('[')
                        var = regex_result[:var_bracket_index]
                        if not variables.__contains__(var):
                            variables.append(var)
                    elif not variables.__contains__(c_var_match.group(1)):
                        variables.append(c_var_match.group(1))

    ############################################# Clojure Program #############################################

    elif file_name.endswith('.clj'):
        cloj_func_ptrn = re.compile(r'\(defn\s+(\w+)-(\w+)')
        cloj_var_ptrn = re.compile(r'\[(\w+(-\w+)?)\s*(\w+)?]')

        file = open(file_name, 'r')
        lines = file.readlines()

        for line in lines:
            if not line.__contains__('//'):
                cloj_func_match = cloj_func_ptrn.search(line)
                if cloj_func_match:
                    cloj_func_string = str(cloj_func_match)
                    apost_index = cloj_func_string.find('\'')
                    regex_result = cloj_func_string[apost_index + 1:-2]

                    func_space_index = regex_result.find(' ')
                    func = regex_result[func_space_index:]

                    if not functions.__contains__(func):
                        functions.append(func)

                cloj_var_match = cloj_var_ptrn.search(line)
                if cloj_var_match:
                    cloj_var_string = str(cloj_var_match)
                    apost_index = cloj_var_string.find('\'')
                    regex_result = cloj_var_string[apost_index + 1:-2]

                    if regex_result.__contains__('['):
                        if regex_result.__contains__(' '):
                            if regex_result.count(' ') == 1:
                                var_space_index = regex_result.find(' ')
                                var1 = regex_result[1:var_space_index]
                                var2 = regex_result[var_space_index + 1:-1]
                                if not variables.__contains__(var1):
                                    variables.append(var1)
                                if not variables.__contains__(var2):
                                    variables.append(var2)
                    if not variables.__contains__(cloj_var_match.group(1)) and line.count('[') < 2:
                        variables.append(cloj_var_match.group(1))

    ############################################# OCaml Program #############################################

    elif file_name.endswith('ml'):
        ocaml_class_ptrn = re.compile(r'(?:type token =|type|\|(?!\s+_))\s+(\w+).*')
        ocaml_func_ptrn = re.compile(r'(?:let|and)\s+((rec\s+)?\w+)\s+(?:(\w+)|\(\))\s+.*=')
        ocaml_var_ptrn = re.compile(r'let\s+(\w+)\s*(?<!_)=\s*.*')

        file = open(target_file, 'r')
        lines = file.readlines()

        for line in lines:
            if not line.__contains__('(*'):
                ocaml_class_match = ocaml_class_ptrn.search(line)
                if ocaml_class_match:
                    if not classes.__contains__(ocaml_class_match.group(1)):
                        classes.append(ocaml_class_match.group(1))

                ocaml_func_match = ocaml_func_ptrn.search(line)
                if ocaml_func_match:
                    ocaml_func_string = str(ocaml_func_match)
                    apost_index = ocaml_func_string.find('\'')
                    regex_result = ocaml_func_string[apost_index + 1:-2]

                    if regex_result.__contains__('rec'):
                        func_rec_index = regex_result.find('rec')
                        func = regex_result[func_rec_index + 4:]
                        func_space_index = func.find(' ')
                        func_name = func[:func_space_index]
                        if not functions.__contains__(func_name):
                            functions.append(func_name)
                    elif not functions.__contains__(ocaml_func_match.group(1)):
                        functions.append(ocaml_func_match.group(1))

                ocaml_var_match = ocaml_var_ptrn.search(line)
                if ocaml_var_match:
                    if not variables.__contains__(ocaml_var_match.group(1)):
                        variables.append(ocaml_var_match.group(1))

    ############################################# ASP Program #############################################

    elif file_name.endswith('.lp'):
        asp_pred_ptrn = re.compile(r'(\w+)\(')
        asp_var_ptrn = re.compile(r'#const\s*(\w+)=.*')

        file = open(target_file, 'r')
        lines = file.readlines()

        for line in lines:
            if not line.__contains__('%'):
                asp_pred_match = asp_pred_ptrn.search(line)
                if asp_pred_match:
                    if not functions.__contains__(asp_pred_match.group(1)):
                        functions.append(asp_pred_match.group(1))

                asp_var_match = asp_var_ptrn.search(line)
                if asp_var_match:
                    if not variables.__contains__(asp_var_match.group(1)):
                        variables.append(asp_var_match.group(1))

    ############################################# Python Program #############################################

    elif file_name.endswith('.py'):
        py_func_ptrn = re.compile(r'def\s+(\w+)\(')
        py_var_ptrn = re.compile(r'(\w+)\s+=\s+.*')

        file = open(target_file, 'r')
        lines = file.readlines()

        for line in lines:
            if not line.__contains__('#'):
                py_func_match = py_func_ptrn.search(line)
                if py_func_match:
                    if not functions.__contains__(py_func_match.group(1)):
                        functions.append(py_func_match.group(1))

                py_var_match = py_var_ptrn.search(line)
                if py_var_match:
                    if not variables.__contains__(py_var_match.group(1)):
                        variables.append(py_var_match.group(1))

    classes.sort()
    functions.sort()
    variables.sort()

    summary_html_template = f"""<html> 
        <head> 
        <title>{html_file_name}</title> 
        </head> 
        <body> 
        <h2>{'File Name: '}<a href={target_file}>{file_name}</a></h2> 
        <h2>{'File Line Count: ' + file_line_count}</h2>
        <h2>List of Classes in this file: </h2> 
        <h3>{print_list(classes)}</h3>
        <h2>List of Functions in this file: </h2> 
        <h3>{print_list(functions)}</h3>
        <h2>List of Variables in this file: </h2> 
        <h3>{print_list(variables)}</h3>
        </body> 
        </html> 
        """

    f.write(summary_html_template)
    f.close()

    return file_name, html_file_name


def read_dir_files(target_directory, f_list):
    os.chdir(target_directory)

    directory_list = os.listdir(target_directory)

    for file in directory_list:
        if os.path.isdir(file):
            read_dir_files(target_directory + '/' + file, f_list)
            os.chdir(target_directory)
        elif file == 'Project1.c':
            file_name, html_file_name = create_html_summary_file(file, 1)
            f_list.append(file_name)
            f_list.append(html_file_name)
        elif file == 'Project2.clj':
            file_name, html_file_name = create_html_summary_file(file, 2)
            f_list.append(file_name)
            f_list.append(html_file_name)
        elif file == 'Project3.ml':
            file_name, html_file_name = create_html_summary_file(file, 3)
            f_list.append(file_name)
            f_list.append(html_file_name)
        elif file == 'Project4.lp':
            file_name, html_file_name = create_html_summary_file(file, 4)
            f_list.append(file_name)
            f_list.append(html_file_name)
        elif file == 'Project5.py':
            file_name, html_file_name = create_html_summary_file(file, 5)
            f_list.append(file_name)
            f_list.append(html_file_name)

    return f_list


if __name__ == '__main__':
    print('Reading Files...')

    file_list = list()

    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    os.chdir(parent_directory)

    source_file_list = read_dir_files(parent_directory, file_list)

    index_file = create_html_index_file()
    source_file_list.append(index_file)

    os.chdir(parent_directory)

    projects = tarfile.open('CSC344ProjectsJackWilcox.tar', 'w:gz')

    for source_file in source_file_list:
        projects.add(source_file)
        os.remove(source_file)

    projects.close()

    print('Complete')

    email_address = input('Enter an Email Address: ')

    subprocess.call(['mutt', '-a', '/home/jwilcox5/csc344/CSC344ProjectsJackWilcox.tar', '-s' 'CSC 344 Project 5 Jack Wilcox', '--', email_address])

    print('Email Sent!')
