# main.py
import myutils                            # 方式①：导入整个包
from myutils import clean_text            # 方式②：直接导入某个函数

def main():
    s = "  Hello WORLD  "

    print("方式① myutils.clean_text ->", myutils.clean_text(s))   # 包名.函数
    print("方式① myutils.count_words ->", myutils.count_words("a b c"))
    print("方式② clean_text ->", clean_text(s))                    # 直接函数名

if __name__ == "__main__":
    main()