from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

registration_number = Annotated[str, mapped_column(String(8))]
business_tax_number = Annotated[str, mapped_column(String(10))]
proprietor_tax_number = Annotated[str, mapped_column(String(12))]