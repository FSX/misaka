from ._md4c import ffi

from .detail import auto_block_detail, auto_span_detail
from .utils import cstr_to_str


ERROR_STATUS_CODE = 1


@ffi.def_extern(error=ERROR_STATUS_CODE)
def _misaka_enter_block(type, detail, userdata):
    session = ffi.from_handle(userdata)
    session.renderer.enter_block(session.buffer, type, detail)
    return 0


@ffi.def_extern(error=ERROR_STATUS_CODE)
def _misaka_leave_block(type, detail, userdata):
    session = ffi.from_handle(userdata)
    session.renderer.leave_block(session.buffer, type, detail)
    return 0


@ffi.def_extern(error=ERROR_STATUS_CODE)
def _misaka_enter_span(type, detail, userdata):
    session = ffi.from_handle(userdata)
    session.renderer.enter_span(session.buffer, type, detail)
    return 0


@ffi.def_extern(error=ERROR_STATUS_CODE)
def _misaka_leave_span(type, detail, userdata):
    session = ffi.from_handle(userdata)
    session.renderer.leave_span(session.buffer, type, detail)
    return 0


@ffi.def_extern(error=ERROR_STATUS_CODE)
def _misaka_text(type, text, size, userdata):
    session = ffi.from_handle(userdata)
    session.renderer.text(
        session.buffer, 
        type, 
        cstr_to_str(text, size), 
    )
    return 0


@ffi.def_extern()
def _misaka_debug_log(msg, userdata):
    session = ffi.from_handle(userdata)
    session.renderer.debug(cstr_to_str(msg))
