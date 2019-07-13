import json
import sys

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

def filter_groups(groups, nr_article, dest_file):
    output = []
    for k in groups:
        len_group = len(groups[k])
        end = nr_article if nr_article <= len_group else len_group
        for i in range(0, end):
            output.append(groups[k][i])
    with open(dest_file, 'w') as dest:
        json.dump(output, dest, ensure_ascii=False)


def report_group_metrics(groups):
    print("The content has {} groups:".format(len(list(groups.keys()))))
    for k in groups:
        print("{} has {} articles".format(k, len(groups[k])))

if __name__ == '__main__':
    if len(sys.argv) <2:
        print("content_filter.py source_file [nr_articles dest_file]")
        exit(1)

    source_file = sys.argv[1]
    contents = load_contents(source_file)
    groups = group_content(contents)
    report_group_metrics(groups)

    if len(sys.argv) == 4:
        nr_articles = int(sys.argv[2])
        dest_file_name = sys.argv[3]
        filter_groups(groups, nr_articles, dest_file_name)