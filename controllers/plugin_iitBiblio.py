# -*- coding: utf-8 -*-
# prova qualcosa come
def index():
    form = SQLFORM.factory(
        Field("title", comment=T("Title filter string")),
        Field("author", comment=T("Author filter string")),
        Field("page_size", "integer", default=5, requires=IS_IN_SET([5, 10, 20, 50, 100])),
        hidden={"page-number": 1},
        _id = "biblio-filter-form"
    )
    form.add_button('Reset', URL())
    if form.validate(keepvalues=True):
        pass
    return dict(form=form)
