"""Create a small sample HR policy PDF for local testing."""

from pathlib import Path

from pypdf import PdfWriter
from pypdf.generic import (
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
    NumberObject,
)

OUTPUT = Path(__file__).resolve().parent / "sample_hr_policy.pdf"

TEXT = """HR Policy Handbook

Leave Policy:
All full-time employees receive 20 days of paid annual leave per year.
Sick leave allowance is 10 days per year.

Probation Period:
New employees serve a probation period of 3 months.

Work Hours:
Standard working hours are 9:00 AM to 6:00 PM, Monday to Friday.
"""


def create_pdf(path: Path) -> None:
    """Create a minimal text PDF without extra dependencies."""
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)

    stream = DecodedStreamObject()
    stream.set_data(
        (
            "BT /F1 12 Tf 50 750 Td "
            "(HR Policy Handbook) Tj "
            "0 -20 Td (Leave Policy: 20 days annual leave, 10 sick days.) Tj "
            "0 -20 Td (Probation Period: 3 months for new employees.) Tj "
            "0 -20 Td (Work Hours: 9 AM to 6 PM, Monday to Friday.) Tj "
            "ET"
        ).encode("latin-1")
    )

    page[NameObject("/Contents")] = stream
    page[NameObject("/Resources")] = DictionaryObject(
        {
            NameObject("/Font"): DictionaryObject(
                {
                    NameObject("/F1"): DictionaryObject(
                        {
                            NameObject("/Type"): NameObject("/Font"),
                            NameObject("/Subtype"): NameObject("/Type1"),
                            NameObject("/BaseFont"): NameObject("/Helvetica"),
                        }
                    )
                }
            )
        }
    )

    writer.write(path)


if __name__ == "__main__":
    create_pdf(OUTPUT)
    print(f"Created: {OUTPUT}")
