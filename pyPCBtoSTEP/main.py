from .board import Board


def main():
    gerbersDir = 'examples/exampleGerbers'
    test = Board(gerbersDir)
    test.open_files()
