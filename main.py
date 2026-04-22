from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


engine = create_engine("sqlite:///:memory:", echo=True)


Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()



class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))


    products = relationship("Product", back_populates="category")



class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


    price = Column(Numeric(10, 2), nullable=False)

    in_stock = Column(Boolean, default=True)


    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")



Base.metadata.create_all(engine)
