from gpt import get_completion, get_single_completion
from readexcel import ExcelData
from fillword import WordFiller

messages = []

def main():
    e = ExcelData()
    w = WordFiller(e)
    w.fill_words()


if __name__ == "__main__":
    main()