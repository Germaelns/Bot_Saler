from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, VARCHAR, PrimaryKeyConstraint, UniqueConstraint, ForeignKey, FLOAT

Base = declarative_base()


class Group(Base):
    __tablename__ = 'group'

    id = Column('id', INTEGER, autoincrement=True)
    vk_group_id = Column('vk_group_id', VARCHAR(50), nullable=False)
    user_id = Column('user_id', INTEGER, ForeignKey("user.id"), nullable=False)

    PrimaryKeyConstraint(id, name='PK_Group_Id')
