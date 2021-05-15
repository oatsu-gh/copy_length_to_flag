#!/usr/bin/env python3
# Copyright (c) 2020 oatsu
"""UTAUのノート長をフラグにコピーする。調声晒しで長さがわかりやすそう。

実行時のバッチファイルで、追加と削除を切り替える。
"""
import re
from sys import argv

import utaupy as up


def copy_length_to_flags(plugin: up.utauplugin.UtauPlugin):
    """ノート長をフラグに追記する

    Length=480(4分音符)で元のフラグが'g-2H40'のとき、
    '【480】g-2H40' みたいな表記になるようにする。
    """
    for note in plugin.notes:
        note.flags = f'【{str(note.length)}】{str(note.flags)}'


def delete_length_to_flags(plugin: up.utauplugin.UtauPlugin):
    """フラグ内のLengthを消す

    '【480】g-2H40' -> 'g-2H40'
    'g-2【480】H40' -> 'g-2H40'
    """
    pattern = '【.*?】'
    for note in plugin.notes:
        note.flags = re.sub(pattern, '', note.flags)


def main(plugin, mode):
    """動作を切り替えるラッパー
    """
    if mode == 'copy':
        delete_length_to_flags(plugin)
        copy_length_to_flags(plugin)
    elif mode == 'delete':
        delete_length_to_flags(plugin)
    else:
        raise ValueError('mode must be "copy" or "delete"')


if __name__ == '__main__':
    # `python copy_length_to_flags.py hogehoge.tmp --mode copy`
    up.utauplugin.run(main, option=argv[3])
