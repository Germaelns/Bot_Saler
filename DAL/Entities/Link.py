from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, VARCHAR, PrimaryKeyConstraint, UniqueConstraint, ForeignKey, FLOAT

Base = declarative_base()


class Link(Base):
    __tablename__ = "link"

    id = Column('id', INTEGER, autoincrement=True)
    image = Column('image', VARCHAR(1000), nullable=False)
    title = Column('title', VARCHAR(1000), nullable=False)
    url = Column('url', VARCHAR(1000), nullable=False)
    price = Column('price', FLOAT, nullable=False)
    sale = Column('sale', INTEGER, nullable=False)
    group_id = Column('group_id', INTEGER, ForeignKey("group.id"), nullable=False)
    user_id = Column('user_id', INTEGER, ForeignKey("user.id"), nullable=False)

    PrimaryKeyConstraint(id, name="PK_Link_Id")
    UniqueConstraint(url, name="UQ_Link_Url")
