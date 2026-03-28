from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Boolean,String,DateTime,Enum,ForeignKey,Integer,Text
from datetime import datetime
import enum

class Base(DeclarativeBase):
    pass

class Role(enum.Enum):
    user  = 'user'
    admin = 'admin'

class CommonBase(Base):
    __abstract__ = True

    id: Mapped[int]             = mapped_column(Integer,primary_key=True)
    is_deleted:Mapped[bool]     = mapped_column(Boolean,default=False)
    is_created:Mapped[datetime] = mapped_column(DateTime,default=datetime.now)

class User(CommonBase):
    __tablename__ = 'user'

    name:Mapped[str]            = mapped_column(String(length=40),nullable=False)
    role:Mapped[Role]           = mapped_column(Enum(Role),default=Role.user)
    profile: Mapped["Profile"]  = relationship(back_populates="user")

class Profile(CommonBase):
    __tablename__ = 'profile'

    profile_url:Mapped[str]     = mapped_column(Text,nullable=True)
    user_id:Mapped[int]         = mapped_column(Integer,ForeignKey('user.id'))
    user:Mapped["User"]         = relationship(back_populates="profile")
