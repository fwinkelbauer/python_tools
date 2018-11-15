import collections
import glob
import re


# TODO what does __slots__ do?
class QueryRepl(collections.namedtuple('QueryRepl', 'query repl')):
    __slots__ = ()


def read_file_lines(file_name, charset, end_of_line):
    with open(file_name, 'r', encoding=charset, newline=end_of_line) as f:
        return f.read().splitlines()


def write_file_lines(file_name, lines, charset, end_of_line):
    with open(file_name, 'w', encoding=charset, newline=end_of_line) as f:
        for line in lines:
            f.write(line + '\n')


def transform_files(glob_pattern, charset, end_of_line, query_repls, log):
    file_names = glob.glob(glob_pattern, recursive=True)
    for file_name in file_names:
        lines = read_file_lines(file_name, charset, end_of_line)
        lines_changed, new_lines = transform_lines(lines, query_repls)
        if (lines_changed):
            log("Wrote file '{}'".format(file_name))
            write_file_lines(file_name, new_lines, charset, end_of_line)
        else:
            log("Skipped file '{}'".format(file_name))


def transform_lines(lines, query_repls):
    new_lines = lines
    lines_changed = False
    for query_repl in query_repls:
        regex = re.compile(query_repl.query)
        tmp_lines = []
        for line in new_lines:
            tmp_line = regex.sub(query_repl.repl, line)
            lines_changed |= tmp_line != line
            tmp_lines.append(tmp_line)
        new_lines = tmp_lines
    return lines_changed, new_lines


query_repls = [
    QueryRepl('<version>.+</version>', '<version>5.0.0</version>'),
    QueryRepl('<title>.+</title>', '<title>Hurr2</title>')]
transform_files('*.nuspec', 'utf-8', '\r\n', query_repls, print)
