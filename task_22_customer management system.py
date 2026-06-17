# 客户管理系统 —— 命令行版

customers = {}  # 存所有客户：{id: {"name":..., "phone":...}}
next_id = 1  # 下一个新客户的 id


def show_menu():
    print("\n===== 客户管理系统 =====")
    print("1. 添加客户")
    print("2. 显示所有客户")
    print("3. 查找客户")
    print("4. 修改客户")
    print("5. 删除客户")
    print("0. 退出")


def add_customer():
    global next_id
    name = input("姓名：")
    phone = input("电话：")
    customers[next_id] = {"name": name, "phone": phone}
    print(f"添加成功，该客户 id 是 {next_id}")
    next_id += 1  # id 用掉一个就往后挪，保证不重复


def show_all():
    if not customers:  # 字典为空
        print("还没有任何客户")
        return
    print("id\t姓名\t电话")
    for cid, info in customers.items():
        print(f"{cid}\t{info['name']}\t{info['phone']}")


def find_customer():
    cid = int(input("要查找的客户 id："))
    if cid in customers:
        info = customers[cid]
        print(f"id={cid}  姓名={info['name']}  电话={info['phone']}")
    else:
        print("没有这个 id 的客户")


def modify_customer():
    cid = int(input("要修改的客户 id："))
    if cid in customers:
        customers[cid]["name"] = input("新姓名：")
        customers[cid]["phone"] = input("新电话：")
        print("修改成功")
    else:
        print("没有这个 id 的客户")


def delete_customer():
    cid = int(input("要删除的客户 id："))
    if cid in customers:
        del customers[cid]  # 从字典里删掉
        print("删除成功")
    else:
        print("没有这个 id 的客户")


def main():
    while True:  # 死循环：一直显示菜单，直到用户选退出
        show_menu()
        choice = input("请选择操作：")
        if choice == "1":
            add_customer()
        elif choice == "2":
            show_all()
        elif choice == "3":
            find_customer()
        elif choice == "4":
            modify_customer()
        elif choice == "5":
            delete_customer()
        elif choice == "0":
            print("再见！")
            break  # 跳出 while，程序结束
        else:
            print("输入有误，请重新选择")

if __name__ == "__main__":
    main()
