#!/usr/bin/env python3
# coding=utf-8
import yaml

COMMENTS_YAML = "./comments.yml"
COLUMN_COMMENTS_YAML = "./column_comments.yml"
DUPLICATE_COLUMN_COMMENTS_YAML = "./duplicate_column_comments.yml"


def get_all_comments():
    """
    すべての項目名と項目名コメント取得する

    Returns
    -------
    comments_list : dict
        {項目名: [項目名コメント, ...], ...}
    """
    with open(COMMENTS_YAML, "r") as f:
        comments_yaml = yaml.safe_load(f)
        tables = comments_yaml["comments"]
        comments_list = {}
        for table in tables:
            column_comments = table["columnComments"]
            for column, comment in list(column_comments.items()):
                comments_list.setdefault(column, set([])).add(comment)
    return comments_list


def write_all_comments_and_duplicate_comments(comments_list):
    """
    項目名コメントに表記ゆれがあるものを出力する

    Parameters
    ----------
    comments_list : dict
        {項目名: [項目名コメント, ...], ...}
    """
    comments_yaml = {}
    duplicates_yaml = {}
    for column, comment in list(comments_list.items()):
        print(column)
        print(comment)
        comments_yaml[column] = " ".join(comment)
        if len(comment) > 1:
            duplicates_yaml[column] = comments_yaml[column]
    with open(DUPLICATE_COLUMN_COMMENTS_YAML, "w") as out:
        out.write(yaml.dump(duplicates_yaml, default_flow_style=False, allow_unicode=True, indent=4))
    with open(COMMENTS_YAML, "w") as out:
        out.write(yaml.dump(comments_yaml, default_flow_style=False, allow_unicode=True, indent=4))


def main():
    print("start.")
    comments_list = get_all_comments()
    print(comments_list)
    write_all_comments_and_duplicate_comments(comments_list)
    print("end.")


if __name__ == '__main__':
    main()
