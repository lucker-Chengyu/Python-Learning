# 定义装饰器
def login_required(func):
    def wrapper(*args, **kwargs):
        if not is_logged_in:
            print("请先登录")
            return
        return func(*args, **kwargs)
    return wrapper

# 多个函数都需要登录验证
is_logged_in = False   # 模拟未登录状态

@login_required
def view_profile():
    print("查看个人资料")

@login_required
def edit_profile():
    print("编辑个人资料")

@login_required
def delete_account():
    print("删除账号")

# 未登录时
view_profile()      # 请先登录
edit_profile()      # 请先登录
delete_account()    # 请先登录

# 登录后
is_logged_in = True
view_profile()      # 查看个人资料
edit_profile()      # 编辑个人资料
delete_account()    # 删除账号


# 优点
# 假设验证逻辑要改，只改装饰器一处
def login_required(func):
    def wrapper(*args, **kwargs):
        if not is_logged_in:
            print("请先登录")
            print("正在跳转登录页面...")  # 加一行，所有函数自动更新
            return
        return func(*args, **kwargs)
    return wrapper