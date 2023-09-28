#!/usr/bin/env python3
# lib/debug.py

from models.classes import CONN, CURSOR, Player, Result
import ipdb

def reset_database():
    Player.drop_table()
    Result.drop_table()
    Player.create_table()
    Result.create_table()


ipdb.set_trace()