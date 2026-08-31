from hwpx import HwpxDocument
from hwpx_agent.models import (
    HwpxModel,
    HwpxHeadingModel,
    HwpxParagraphModel,
    HwpxTableModel,
)


def model_to_hwpx(hwpx_model: HwpxModel) -> HwpxDocument:

    hwpx_document: HwpxDocument = HwpxDocument.new()

    for content in hwpx_model.contents:
        if isinstance(content, HwpxHeadingModel):
             hwpx_document.add_heading(content.text, level=content.level)

        elif isinstance(content, HwpxParagraphModel):
            char_pr_id = hwpx_document.styles.ensure_run(
                size=content.style.size,
                italic=content.style.italic,
                underline=content.style.underline,
                color=content.style.color,
                font=content.style.font,
                highlight=content.style.highlight,
                strike=content.style.strike,
                underline_shape=content.style.underline_shape,
                underline_color=content.style.underline_color,
                strike_shape=content.style.strike_shape,
                ratio=content.style.ratio,
                letter_spacing=content.style.letter_spacing,
                shadow=content.style.shadow,
                script=content.style.script,
                outline=content.style.outline,
                emboss=content.style.emboss,
                engrave=content.style.engrave,
            )

            paragraph = hwpx_document.add_paragraph(
                text="",
                style_id_ref=0,
                para_pr_id_ref=0,
            )

            paragraph.add_run(text=content.text, char_pr_id_ref=char_pr_id)

        elif isinstance(content, HwpxTableModel):

            section = hwpx_document.add_section()

            paragraph = section.add_paragraph()

            table = paragraph.add_table(rows=content.rows, cols=content.cols)

            for element in content.elements:
                cell = table.cell(row_index=element.row, col_index=element.col)
                cell.add_paragraph(text=element.text)


    return hwpx_document