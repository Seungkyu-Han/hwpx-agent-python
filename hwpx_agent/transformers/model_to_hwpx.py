from hwpx import HwpxDocument
from hwpx_agent.models import HwpxModel, HwpxHeadingModel


def model_to_hwpx(hwpx_model: HwpxModel) -> HwpxDocument:

    hwpx_document: HwpxDocument = HwpxDocument.new()

    for paragraph in hwpx_model.content:
        if isinstance(paragraph, HwpxHeadingModel):
            hwpx_document.add_heading(paragraph.text, level=paragraph.level)

        else:

            style_id = hwpx_document.styles.ensure_run(
                size=paragraph.style.size,
                italic=paragraph.style.italic,
                underline=paragraph.style.underline,
                color=paragraph.style.color,
                font=paragraph.style.font,
                highlight=paragraph.style.highlight,
                strike=paragraph.style.strike,
                underline_shape=paragraph.style.underline_shape,
                underline_color=paragraph.style.underline_color,
                strike_shape=paragraph.style.strike_shape,
                ratio=paragraph.style.ratio,
                letter_spacing=paragraph.style.letter_spacing,
                shadow=paragraph.style.shadow,
                script=paragraph.style.script,
                outline=paragraph.style.outline,
                emboss=paragraph.style.emboss,
                engrave=paragraph.style.engrave,
            )

            hwpx_document.add_paragraph(paragraph.text, style=style_id)


    return hwpx_document