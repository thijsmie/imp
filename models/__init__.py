from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from . import relation, transaction, stock, product, margin, note, right

__all__ = ["relation", "transaction", "stock", "product", "margin", "note", "right"]

Relation = relation.Relation
Transaction = transaction.Transaction
Stock = stock.Stock
Product = product.Product
Margin = margin.Margin
Note = note.Note
Right = right.Right