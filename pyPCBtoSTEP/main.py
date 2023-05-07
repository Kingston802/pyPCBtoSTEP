from .board import Board


def main():
    gerbersDir = 'examples/exampleGerbers'
    test = Board(gerbersDir)
    test.open_files()

    # draw copper
    cu_weight = 2  # oz
    test.draw_copper(cu_weight)
