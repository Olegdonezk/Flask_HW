from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Numeric,
    func
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


engine = create_engine("sqlite:///:memory:", echo=False)


Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


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
    price = Column(Numeric(10, 2))  # фиксированная точность
    in_stock = Column(Boolean, default=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")



Base.metadata.create_all(engine)




electronics = Category(name="Электроника", description="Гаджеты и устройства.")
books = Category(name="Книги", description="Печатные книги и электронные книги.")
clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")

session.add_all([electronics, books, clothes])
session.commit()


products = [
    Product(name="Смартфон", price=299.99, in_stock=True, category=electronics),
    Product(name="Ноутбук", price=499.99, in_stock=True, category=electronics),
    Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=books),
    Product(name="Джинсы", price=40.50, in_stock=True, category=clothes),
    Product(name="Футболка", price=20.00, in_stock=True, category=clothes),
]

session.add_all(products)
session.commit()


print("\n=== Категории и продукты ===")
categories = session.query(Category).all()

for cat in categories:
    print(f"\nКатегория: {cat.name}")
    for p in cat.products:
        print(f" - {p.name} | {p.price}")


smartphone = session.query(Product).filter_by(name="Смартфон").first()
if smartphone:
    smartphone.price = 349.99
    session.commit()


print("\n=== Количество продуктов по категориям ===")

result = (
    session.query(Category.name, func.count(Product.id))
    .join(Product)
    .group_by(Category.id)
    .all()
)

for name, count in result:
    print(f"{name}: {count}")


print("\n=== Категории с >1 продуктом ===")

filtered = (
    session.query(Category.name, func.count(Product.id).label("cnt"))
    .join(Product)
    .group_by(Category.id)
    .having(func.count(Product.id) > 1)
    .all()
)

for name, cnt in filtered:
    print(f"{name}: {cnt}")
