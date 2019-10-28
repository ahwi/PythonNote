from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)


Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                             self.name, self.fullname, self.password)


def add_object():
    Base.metadata.create_all(engine)
    session = Session()
    # 添加
    ed_user = User(name='ed', fullname='Ed Jones', password='edpassword')
    session.add(ed_user)

    # 查询
    our_user = session.query(User).filter_by(name='ed').first()
    # print(our_user)

    # 添加多个
    session.add_all([
        User(name='wndy', fullname='Wndy Williams', password='foobar'),
        User(name='mary', fullname='Mary Contrary', password='xxg527'),
        User(name='fred', fullname='Fred Flinstone', password='edpassword')
    ])

    # 修改某个字段
    ed_user.password = 'f8s7ccs'
    # print("[dirty]:", session.dirty)
    # print("[new]", session.new)
    session.commit()

    # 查看ed的id 变成有值
    # print(ed_user.id)

    # 回滚
    ed_user.name = 'Edwardo'
    fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
    session.add(fake_user)
    session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()

    session.rollback()
    print("ed name:", ed_user.name)

    print(
        "select:",
        session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()
    )

    # 查询
    print("###query:")
    # for instance in session.query(User).order_by(User.id):
    #     print(instance.name, instance.fullname)

    # query 返回的是命名的tuple
    # for row in session.query(User, User.name).all():
    #     print(row)
    #     # print(row.User, row.name)

    # # 使用label()结构控制单个列表的名称
    # for row in session.query(User.name.label('name_label')).all():
    #     print(row.name_label)

    # # 假设在对query()存在多个实体，可以使用aliased()来控制实体 如User
    # from sqlalchemy.orm import aliased
    # user_alias = aliased(User, name='user_alias')
    # for row in session.query(user_alias, user_alias.name).all():
    #     print(row.user_alias)

    # # LIMIT 和 OFFSET 操作
    # for u in session.query(User).order_by(User.id)[1:3]:
    #     print(u)

    # 过滤结果: filter_by() 使用关键字过滤; filter() 使用SQL表达式语言结构
    for name in session.query(User.name).filter_by(fullname='Ed Jones'):
        print(name)

    for name in session.query(User.name).filter(User.fullname=='Ed Jones'):
        print(name)

    # query 对象完全生成:大多数方法调用返回一个新的Query对象
    for user in session.query(User).\
            filter(User.name == 'ed').\
            filter(User.fullname == "Ed Jones"):
        print(user)


class Student:
    def __init__(self):
        name = 'jack'
        age = 18


def test_code():
    jack = Student()
    row = (jack, 'rose')
    print(row.name, row.age)



if __name__ == "__main__":
    add_object()
    # test_code()

