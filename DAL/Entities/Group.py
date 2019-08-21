from sqlalchemy import Column, INTEGER, VARCHAR, PrimaryKeyConstraint, ForeignKey
from DAL.meta import Base


class Group(Base):
    __tablename__ = 'group'

    id = Column('id', INTEGER, autoincrement=True)
    name = Column('name', VARCHAR(100), nullable=False)
    vk_group_id = Column('vk_group_id', VARCHAR(50), nullable=False)
    user_id = Column('user_id', INTEGER, ForeignKey("user.id"), nullable=False)

    PrimaryKeyConstraint(id, name='PK_Group_Id')
