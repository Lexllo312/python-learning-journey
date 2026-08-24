
import logging    #配置日志

#配置一次：INFO 及以上才显示，格式化带时间戳+级别
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

#建 logger（惯例用 __name__）
logger = logging.getLogger(__name__)

# 自定义错误：继承 ValueError（也可以是 Exception 或其他内置异常）
class NegativeNumberError(ValueError):
    pass

#内置错误是 Python 帮你定义好的"通用出错"，自定义错误是你为"你的业务规则"专门造的错。
'''
raise = 主动"抛出"一个错误，自定义错误 = 写一个继承自 Exception 的类
读报错: traceback从上往下读, 最下面的File "xxx.py", line N才是出错点
'''
def check_age(age):
    if not isinstance(age, int):
        raise ValueError("错误，年龄要求整数")    #内置错误

    if age < 0:
        raise NegativeNumberError("错误，年龄不能为负")    #自定义错误
    
    return age

def main():
        '''
        try----总是先执行----放可能出错的代码
        except 异常 as e----匹配到对应异常时----捕获并处理错误
        else----try 里没抛错才执行----放"成功后要做的"逻辑
        finally----无论是否抛错都执行----放"收尾/清理"（比如关文件）
        '''
        try:

            #input 键盘输入
            age_str = input("请输入年龄：")
            age = int(age_str) 
            result = check_age(age)
        except NegativeNumberError as e:
            
            #logger.info 为print的升级版，带调试
            logger.info(f"except(NegativeNumberError): {e}")

        except ValueError as e:
            logger.info(f"except(ValueError): {e}")

        else:
            logger.info(f"else: 年龄合法 = {result}")

        finally:
            logger.info("finally: 收尾")


if __name__ == "__main__":
    main()