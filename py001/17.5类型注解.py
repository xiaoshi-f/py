# 电商订单计算器功能（商品信息，数量，价格）（优惠，优惠券，积分抵扣）运费信息
 # 优惠券满5000以后用,优惠券价格不超过商品总价
 # 积分满5000以后用,100积分抵扣1元(整百抵扣)抵扣金额不超过商品总价
def jisun(coupon=0,score=0,espress=0,*args: tuple[str,float,int]):

    """
    :param args: （商品名称，数量goods[1]，价格goods[2]）args  goods[1] * goods[2]
    :param coupon:优惠券
    :param score:积分
    :param espress:运费
    :return:订单总金额
    订单用金额=商品总金额-优惠券-积分+运费
    """
    # 1,商品总金额每一个商品 价格*数量,定义一个列表
    total_price = [goods[1] * goods[2] for goods in args]
    total_cost = sum(total_price)# 总金额
    # 2,扣减优惠券
    if total_cost >= 5000 and coupon <= total_cost:
        total_cost -= coupon
# 3,扣减积分抵扣
    if total_cost >= 5000 and score //100 <= total_cost:
        total_cost -= score // 100
# 4,添加运费
    total_cost += espress

    return total_cost
shi=jisun(100,1000,10000,("鼠标",188.8,2),("键盘",128,6),("电脑",1999,10))
print('JIAG',shi)
# 类型提示 明确表示变量,函数参数,返回值的数据类型
# a:int =19  name: list[str]=["a","s","d"]     shi: list[str | int]
# 函数的类型注解    函数类型    返回值类型
def jisun(ni: list[int]) ->float:
    return sum(ni)/len(ni)