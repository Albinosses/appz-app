from .pages import *
from . import styles

import reflex as rx

app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
)
