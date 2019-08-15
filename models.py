from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, VARCHAR, PrimaryKeyConstraint, UniqueConstraint

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column('id', INTEGER, autoincrement=True)
    login = Column('login', VARCHAR(30), nullable=False)
    password = Column('password', VARCHAR(50), nullable=False)
    vk_token = Column('vk_token', VARCHAR(200), nullable=False)
    epn_token = Column('epn_token', VARCHAR(200), nullable=False)
    start_timer = Column('start_timer', VARCHAR(5), nullable=False)
    end_timer = Column('end_timer', VARCHAR(5), nullable=False)
    last_post_time = Column('last_post_time', VARCHAR(200), nullable=False)

    PrimaryKeyConstraint(id, name='PK_Group_Id')
    UniqueConstraint(login, name="UQ_User_login")
    UniqueConstraint(vk_token, name="UQ_User_vk_token")
    UniqueConstraint(epn_token, name="UQ_User_epn_token")


