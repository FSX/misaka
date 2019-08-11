from dataclasses import dataclass, field, fields

from . import const
from ._md4c import ffi
from .types import char, Attribute
from .utils import cstr_to_str


def _ctype_field(value):
    return field(
        default=value,
        init=False,
        repr=False,
    )


@dataclass
class BaseDetail:
    @classmethod
    def from_c(cls, c_obj):
        c_obj = ffi.cast(cls.ctype, c_obj)
        args = {}

        for field in fields(cls):
            if field.name == 'ctype':
                continue
            if field.type in (bool, int):
                args[field.name] = getattr(c_obj, field.name)
            elif field.type == char:
                value = getattr(c_obj, field.name).decode('utf-8')
                if value == '\x00':
                    value = ''
                args[field.name] = value
            elif field.type == Attribute:
                args[field.name] = _c_attr_py_attr(getattr(c_obj, field.name))
            else:
                raise TypeError(f'{field.name} of type {field.type} not supported')

        return cls(**args)


def _c_attr_py_attr(c_obj):
    attr = Attribute([])
    ptr = c_obj.text

    n = 0
    while c_obj.substr_offsets[n] < c_obj.size:
        ftype = c_obj.substr_types[n]
        offset = c_obj.substr_offsets[n]
        size = c_obj.substr_offsets[n+1] - offset
        ptr = ptr + offset
        attr.parts.append(Attribute.Part(
            cstr_to_str(ptr, size),
            ftype,
        ))
        n += 1

    return attr


class BlockDetail:
    @dataclass
    class Ul(BaseDetail):
        ctype: str = _ctype_field('MD_BLOCK_UL_DETAIL *')
        is_tight: bool
        mark: char

    @dataclass
    class Ol(BaseDetail):
        ctype: str = _ctype_field('MD_BLOCK_OL_DETAIL *')
        start: int
        is_tight: bool
        mark_delimiter: char

    @dataclass
    class Li(BaseDetail):
        ctype: str = _ctype_field('MD_BLOCK_LI_DETAIL *')
        is_task: bool
        task_mark: char
        task_mark_offset: int

    @dataclass
    class H(BaseDetail):
        ctype: str = _ctype_field('MD_BLOCK_H_DETAIL *')
        level: int

    @dataclass
    class Code(BaseDetail):
        ctype: str = _ctype_field('MD_BLOCK_CODE_DETAIL *')
        info: Attribute
        lang: Attribute
        fence_char: char

    @dataclass
    class Td(BaseDetail):
        ctype: str = _ctype_field('MD_BLOCK_TD_DETAIL *')
        align: int


class SpanDetail:
    @dataclass
    class A(BaseDetail):
        ctype: str = _ctype_field('MD_SPAN_A_DETAIL *')
        href: Attribute
        title: Attribute

    @dataclass
    class Img(BaseDetail):
        ctype: str = _ctype_field('MD_SPAN_IMG_DETAIL *')
        src: Attribute
        title: Attribute


_block_type_detail_mapping = {
    const.BLOCK_UL: BlockDetail.Ul,
    const.BLOCK_OL: BlockDetail.Ol,
    const.BLOCK_LI: BlockDetail.Li,
    const.BLOCK_H: BlockDetail.H,
    const.BLOCK_CODE: BlockDetail.Code,
    const.BLOCK_TH: BlockDetail.Td,
    const.BLOCK_TD: BlockDetail.Td,
}


_span_type_detail_mapping = {
    const.SPAN_A: SpanDetail.A,
    const.SPAN_IMG: SpanDetail.Img,
}


def auto_block_detail(type, detail):
    if detail == ffi.NULL:
        return None
    cls = _block_type_detail_mapping.get(type)
    if cls is None:
        return None
    return cls.from_c(detail)


def auto_span_detail(type, detail):
    if detail == ffi.NULL:
        return None
    cls = _span_type_detail_mapping.get(type)
    if cls is None:
        return None
    return cls.from_c(detail)
