import uuid

import sqlalchemy as sa


class IntegerIDMixin:
    id = sa.Column(
        sa.Integer,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
