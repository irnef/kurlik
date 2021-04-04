from sqlalchemy.orm import session
from sqlalchemy_continuum import Operation

article = Article(name=u'Some article')
session.add(article)
session.commit()

article.versions[0].operation_type == Operation.INSERT

article.name = u'Some updated article'
session.commit()
article.versions[1].operation_type == Operation.UPDATE

session.delete(article)
session.commit()
article.versions[2].operation_type == Operation.DELETE