#!/usr/bin/env python3

import argparse
import collections
import configparser
import glob
import re


class Config(collections.namedtuple(
        'Config', 'file_names charset end_of_line regex_list')):
    __slots__ = ()


def parse_arguments():
    arg_parser = argparse.ArgumentParser(
        description='Search and replace text in files')
    arg_parser.add_argument(
        '-p', '--profile', help='The store profile', default='DEFAULT')
    return arg_parser.parse_args()


def expand_curly(line):
    match = re.search('{([^{]*?)}', line)
    expanded_lines = []
    if match is None:
        expanded_lines.append(line)
    else:
        snippets = match.group(1).split(',')
        for snippet in snippets:
            expanded_lines.append(
                line[:match.start()] + snippet + line[match.end():])
    return expanded_lines


def fetch_files(glob_pattern):
    expanded_patterns = expand_curly(glob_pattern)
    file_names = []
    [file_names.extend(
        glob.glob(p, recursive=True)) for p in expanded_patterns]
    return file_names


def parse_config(text):
    config_parser = configparser.ConfigParser()
    config_parser.read_string(text)
    config_list = []
    for section in config_parser.sections():
        file_names = fetch_files(section)
        section_data = config_parser[section]
        charset = section_data.get('charset')
        end_of_line_text = section_data.get('end_of_line')
        if end_of_line_text is None:
            end_of_line = None
        elif end_of_line_text == 'lf':
            end_of_line = '\n'
        elif end_of_line_text == 'crlf':
            end_of_line = '\r\n'
        else:
            raise ValueError(
                "Supported end of line characters: 'lf' and 'crlf'")
        regex_list_text = section_data.get('regex', '').splitlines()
        regex_list = [re.compile(r) for r in regex_list_text]
        config_list.append(
            Config(file_names, charset, end_of_line, regex_list))
    return tuple(config_list)


def parse_store(text, section_name):
    config_parser = configparser.ConfigParser()
    config_parser.read_string(text)
    return dict(config_parser[section_name])


def read_file_lines(file_name, charset, end_of_line):
    with open(file_name, 'r', encoding=charset, newline=end_of_line) as f:
        return f.read().splitlines()


def write_file_lines(file_name, lines, charset, end_of_line):
    with open(file_name, 'w', encoding=charset, newline=end_of_line) as f:
        for line in lines:
            f.write(line + '\n')


def replace_line(regex, line, store):
    match = regex.search(line)
    replaced_line = line
    line_changed = False
    offset = 0
    if match is not None:
        group_dict = match.groupdict()
        for group_name in group_dict.keys():
            if group_name in store:
                old_value_len = len(match.group(group_name))
                new_value = store[group_name]
                start_index = offset + match.start(group_name)
                end_index = start_index + old_value_len
                start = replaced_line[:start_index]
                end = replaced_line[end_index:]
                replaced_line = start + new_value + end
                line_changed = line != replaced_line
                offset += len(new_value) - old_value_len
    return line_changed, replaced_line


def search_and_replace(config, store, read_file, write_file, log):
    for entry in config:
        for file_name in entry.file_names:
            new_lines = []
            file_dirty = False
            for line in read_file(file_name, entry.charset, entry.end_of_line):
                new_line = line
                for regex in entry.regex_list:
                    line_changed, new_line = replace_line(
                        regex, new_line, store)
                    file_dirty |= line_changed
                new_lines.append(new_line)
            if file_dirty:
                write_file(
                    file_name, new_lines, entry.charset, entry.end_of_line)
                log("Wrote file '{}'".format(file_name))
            else:
                log("Skipped file '{}'".format(file_name))


def main():
    args = parse_arguments()
    with open('nilesstore.ini', 'r') as f:
        store = parse_store(f.read(), args.profile)
    with open('nilesconfig.ini', 'r') as f:
        config = parse_config(f.read())
    search_and_replace(
        config, store, read_file_lines, write_file_lines, print)


if __name__ == '__main__':
    main()
