import io
from render import render_winner_image


class TestRenderWinnerImage:
    def test_returns_png_bytes(self):
        result = render_winner_image(12345, "testuser", "Test User", "Great post!")
        assert isinstance(result, io.BytesIO)
        assert result.name == "winner.png"

    def test_png_header(self):
        result = render_winner_image(1, "u", "N", "comment")
        data = result.read()
        assert data[:4] == b"\x89PNG"

    def test_long_comment_does_not_crash(self):
        long_text = "x" * 500
        result = render_winner_image(1, "u", "N", long_text)
        assert isinstance(result, io.BytesIO)

    def test_empty_fields(self):
        result = render_winner_image(0, "", "", "")
        assert isinstance(result, io.BytesIO)
