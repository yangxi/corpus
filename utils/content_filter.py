import json
import sys
import argparse
import re

def load_contents(fname):
    with open(fname, 'r') as sf:
        contents = json.load(sf)
        return contents
    return []

def group_content(contents, key="catalogue"):
    groups = {}
    for c in contents:
        k = c[key]
        if k in groups:
            groups[k].append(c)
        else:
            groups[k] = [c]
    return groups

def get_first_w(name):
    g = re.search(r'[\w]+', name)
    if g:
        return g.group(0)
    else:
        return g

def catalogue_groups(groups, file_prefix):
    for k in groups:
        file_name = file_prefix + get_first_w(k) + '.json'
        articles = groups[k]
        with open(file_name, 'w') as dest:
            print("Output {} articles in catalogue {} to file {}".format(len(articles), k, file_name))
            json.dump(articles, dest, ensure_ascii=False)

# def filter_groups(groups, nr_article, dest_file):
#     output = []
#     for k in groups:
#         len_group = len(groups[k])
#         end = nr_article if nr_article <= len_group else len_group
#         for i in range(0, end):
#             output.append(groups[k][i])
#     with open(dest_file, 'w') as dest:
#         json.dump(output, dest, ensure_ascii=False)

def report_group_metrics(groups):
    print("The content has {} groups:".format(len(list(groups.keys()))))
    for k in groups:
        print("{} has {} articles".format(k, len(groups[k])))

# content_filter.py article dest_file
# content_filter.py catalogue
if __name__ == '__main__':
    usage = """
    python content_filter.py source_file catalogue dest_file_prefix
    This program generates one JSON file named dest_file_prefix-CATALOGUE.json for each catalogue.
    """
    if len(sys.argv) <2:
        print(usage)
        exit(1)

    source_file = sys.argv[1]
    contents = load_contents(source_file)
    groups = group_content(contents)
    report_group_metrics(groups)

    if sys.argv[2].find('catalogue') != -1:
        file_prefix = None
        if len(sys.argv) > 3:
            file_prefix = sys.argv[3]
        else:
            print(usage)
            exit(1)
        catalogue_groups(groups, file_prefix)
