from sqlalchemy import Column, String, ForeignKey, DateTime, Integer,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    age = Column(Integer, nullable=True)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    disabled = Column(Boolean, default=False)

    # Relationship to images and votes
    images = relationship("Image", back_populates="user")
    votes = relationship("Vote", back_populates="user")


class Image(Base):
    __tablename__ = "image"

    id = Column(String, primary_key=True, index=True)
    image_name = Column(String, index=True)
    image_desc = Column(String)
    image_path = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    rating = Column(Integer)
    disabled = Column(Boolean, default=False)

    # Foreign Key relationship with User
    user_id = Column(String, ForeignKey("user.id"))

    # Relationship to users
    user = relationship("User", back_populates="images")
 

class Vote(Base):
    __tablename__ = "vote"
    id = Column(String, primary_key=True, index=True)
    voter_id = Column(String, ForeignKey("user.id"))
    image1_id = Column(String, ForeignKey("image.id"))
    image2_id = Column(String, ForeignKey("image.id"))
    score_image1 = Column(Integer)
    score_image2 = Column(Integer)
    voted_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    disabled = Column(Boolean, default=False)

    # Relationship to images and users
    image1 = relationship("Image", foreign_keys=[image1_id])
    image2 = relationship("Image", foreign_keys=[image2_id])
    user = relationship("User", back_populates="votes")
