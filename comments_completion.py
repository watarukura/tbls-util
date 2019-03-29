#!/usr/bin/env python3
# coding=utf-8
import yaml

COMMENTS_YAML = "./comments.yml"
COLUMN_COMMENTS_YAML = "./column_comments.yml"
LINT_RESULT = "./lint_result"


def get_completion_target():
    """
    項目名コメントが未入力のレコードを抽出する

    Returns
    -------
    table_column_list : list
        [{"table": テーブル名, "column": 項目名}, ...]
    """
    table_column_list = []
    with open(LINT_RESULT, "r") as f:
        for row in f:
            lint_result = row.split(" ")
            if len(lint_result) > 1 and lint_result[1] == "column":
                table, column_with_colon = lint_result[0].split(".")
                table_column = {"table": table, "column": column_with_colon[0:-1]}
                table_column_list.append(table_column)
        return table_column_list


def add_column_comment(table_column_list):
    """
    既存の項目名コメントを付与する
    既存の項目名が付与できない場合は###を付与する

    Parameters
    ----------
    table_column_list : list
        [{"table": テーブル名, "column": 項目名}, ...]

    Returns
    -------
    table_column_comment_list : list
        [{"table": テーブル名, "column": 項目名, "columnComment": 項目名コメント}, ...]
    """
    table_column_comment_list = []
    with open(COLUMN_COMMENTS_YAML, "r") as f:
        column_comments = yaml.safe_load(f)
    for table_column in table_column_list:
        comment = column_comments.get(table_column["column"], '###')
        if ' ' in comment:
            table_column["columnComment"] = comment.split(" ")[0]
        else:
            table_column["columnComment"] = comment
        table_column_comment_list.append(table_column)
    return table_column_comment_list


def update_comment_yaml(table_column_comment_list):
    """
    comments.ymlに付与した項目名を反映する

    Parameters
    ----------
    table_column_comment_list : list
        [{"table": テーブル名, "column": 項目名, "columnComment": 項目名コメント}, ...]
    """
    with open(COMMENTS_YAML, "r") as f:
        comments_yaml = yaml.safe_load(f)
        for row in comments_yaml["comments"]:
            for target in table_column_comment_list:
                if row["table"] == target["table"]:
                    if "columnComments" in row:
                        row["columnComments"][target["column"]] = target["columnComment"]
                    else:
                        row["columnComments"] = {target["column"]: target["columnComment"]}
        with open(COMMENTS_YAML, "w") as out:
            out.write(yaml.dump(comments_yaml, default_flow_style=False, allow_unicode=True, indent=4))


def get_completion_table_target():
    """
    テーブル名コメントが未入力のテーブルを抽出する

    Returns
    -------
    table_list : list
        [テーブル名, ...]
    """
    table_list = []
    with open(LINT_RESULT, "r") as f:
        for row in f:
            lint_result = row.split(" ")
            if len(lint_result) > 1 and lint_result[1] == "table":
                table = lint_result[0].split(":")[0]
                table_list.append(table)
        return table_list


def update_comment_yaml_for_table_comment(table_list):
    """
    comments.ymlに付与したテーブル名を反映する

    Parameters
    ----------
    table_list : list
        [テーブル名, ...]
    """
    with open(COMMENTS_YAML, "r") as f:
        comments_yaml = yaml.safe_load(f)
        for table in table_list:
            comments_yaml["comments"].append({"table": table, "tableComment": "###"})
        with open(COMMENTS_YAML, "w") as out:
            out.write(yaml.dump(comments_yaml, default_flow_style=False, allow_unicode=True, indent=4))


def main():
    print("start.")
    table_column_list = get_completion_target()
    table_column_comment_list = add_column_comment(table_column_list)
    table_list = get_completion_table_target()
    update_comment_yaml_for_table_comment(table_list)
    update_comment_yaml(table_column_comment_list)
    print("end.")


if __name__ == '__main__':
    main()
