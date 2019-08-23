from sqlalchemy import Column, INTEGER, VARCHAR, PrimaryKeyConstraint, UniqueConstraint, BOOLEAN
from DAL.meta import Base


class User(Base):
    __tablename__ = 'user'

    id = Column('id', INTEGER, autoincrement=True)
    login = Column('login', VARCHAR(50), nullable=False)
    password = Column('password', VARCHAR(50), nullable=False)
    tg_channel = Column('tg_channel', VARCHAR(30), nullable=False)
    active = Column('active', BOOLEAN, nullable=False)
    vk_token = Column('vk_token', VARCHAR(200), nullable=False)
    epn_api_token = Column('epn_api_token', VARCHAR(200), nullable=False)
    epn_hash = Column('epn_hash', VARCHAR(200), nullable=False)
    start_timer = Column('start_timer', INTEGER, nullable=False)
    end_timer = Column('end_timer', INTEGER, nullable=False)
    last_post_time = Column('last_post_time', VARCHAR(200), nullable=False)
    post_iteration_counter = Column('post_iteration_counter', INTEGER, nullable=False)
    post_iteration = Column('post_iteration', INTEGER, nullable=False)

    PrimaryKeyConstraint(id, name='PK_User_Id')
    UniqueConstraint(login, name="UQ_User_Login")
    UniqueConstraint(vk_token, name="UQ_User_Vk_token")
    UniqueConstraint(epn_hash, name="UQ_User_Epn_hash")
    UniqueConstraint(epn_api_token, name="UQ_User_Epn_api_token")
