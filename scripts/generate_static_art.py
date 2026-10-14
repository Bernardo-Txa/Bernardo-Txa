from __future__ import annotations

import make_header_svg
import make_info_card
import make_portrait_svg
import render_heatmap_svg


def main() -> None:
    make_header_svg.main()
    make_portrait_svg.main()
    make_info_card.main()
    render_heatmap_svg.main()


if __name__ == "__main__":
    main()
