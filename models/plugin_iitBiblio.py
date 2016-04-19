# -*- coding: utf-8 -*-

from gluon.tools import fetch
from gluon.contrib.simplejson import JSONDecoder
import re

url = "http://backend.publications.iit.it/api/publications/getMatchingOnesAsJsonData"

class scroller(object):
    """"""

    fields = ["id", "title", "authors", "year", "publication", "references", "doi", "published"]
    alias = {"authors": "author"}
    #paginate = 5

    @classmethod
    def _fetch(cls, page_size=5, **data):
        return JSONDecoder().decode(fetch(url, data=dict({"page-number": 1, "page-size": int(page_size)}, **{k: v for k,v in data.iteritems() if v and not k.startswith("_")})))

    @classmethod
    def _Header(cls):
        return THEAD(TR(*[TH(T(i.title())) for i in cls.fields]))

    @classmethod
    def _Table(cls, data, **kw):

        def _highlights(d, fn):
            k = cls.alias.get(fn, fn)
            if k in kw and kw[k]:
                v = re.sub("(?i)%s" % kw[k], TAG.mark(STRONG(kw[k].upper())).xml(), d[fn])
                #v = d[k].replace(kw[k], TAG.mark(kw[k]).xml())
            else:
                v = d[fn]
            return XML(v)

        return TABLE(cls._Header(), *[[TD(_highlights(o, k)) for k in cls.fields] for o in data], _class="web2py_grid")

    @classmethod
    def paginator(cls, tot, page_size=5, **kw):
        ps = int(page_size)
        ipages = tot/ps
        rpages = tot%ps
        first_page = 1
        last_page = ipages if rpages==0 else ipages+1
        pn = int(request.vars.get("page-number") or 1)
        pn_minus = first_page if pn==first_page else pn-1
        pn_plus = last_page if pn==last_page else pn+1
        FST = LI(A("<<", _title=T("First page"), _href=URL(args=request.args, vars=dict(request.vars, **{"page-number": 0})), cid=request.cid))
        BCK = LI(A("-", _title=T("Previous page"), _href=URL(args=request.args, vars=dict(request.vars, **{"page-number": pn_minus})), cid=request.cid))
        FFW = LI(A("+", _title=T("Next page"), _href=URL(args=request.args, vars=dict(request.vars, **{"page-number": pn_plus})), cid=request.cid))
        LST = LI(A(">>", _title=T("Last page"), _href=URL(args=request.args, vars=dict(request.vars, **{"page-number": last_page})), cid=request.cid))
        SLT = SELECT(range(first_page, last_page+1), _name="page-number", value=pn,
            _title = T("Choose a page"),
            _onchange = '$("input[name=page-number]").val(this.value); $("#biblio-filter-form").submit();'
        )
        if tot >= ps:
            start = pn*ps-ps+1
            end = pn*ps if pn < last_page else tot
        else:
            start = 1
            end = tot
        return start, end, DIV(UL(FST, BCK, SLT, FFW, LST), _class="web2py_paginator")

    @classmethod
    def run(cls, **kw):
        res = cls._fetch(**kw)
        items_count = 0 if not "data" in res else res["items_count"]
        data = [] if not "data" in res else res["data"]
        start, end, paginator = cls.paginator(items_count, **kw)
        return DIV(
            DIV(start, " - ", end, " / ", STRONG(T("%s %%{record} found", symbols=items_count)), _class="web2py_counter"),
            DIV(
                DIV(
                    cls._Table(data, **kw),
                    _class = "web2py_htmltable",
                    _style = "width:100%;overflow-x:auto;-ms-overflow-x:scroll"
                ),
                _class="web2py_table"
            ),
            paginator,
            _class="web2py_grid"
        )

@service.run
def iitws(**kw):
    """ """
    return scroller.run(**request.vars)
