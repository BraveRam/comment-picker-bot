import pytest
from comments import extract_public_post_link, dedupe_comments_by_user


class TestExtractPublicPostLink:
    def test_full_https_link(self):
        username, post_id = extract_public_post_link("https://t.me/channel/123")
        assert username == "channel"
        assert post_id == 123

    def test_http_link(self):
        username, post_id = extract_public_post_link("http://t.me/mychannel/456")
        assert username == "mychannel"
        assert post_id == 456

    def test_link_without_protocol(self):
        username, post_id = extract_public_post_link("t.me/test_channel/789")
        assert username == "test_channel"
        assert post_id == 789

    def test_link_with_surrounding_text(self):
        username, post_id = extract_public_post_link("Check this out: https://t.me/news/42 cool!")
        assert username == "news"
        assert post_id == 42

    def test_no_link(self):
        username, post_id = extract_public_post_link("Hello, no link here")
        assert username is None
        assert post_id is None

    def test_empty_string(self):
        username, post_id = extract_public_post_link("")
        assert username is None
        assert post_id is None

    def test_none_input(self):
        username, post_id = extract_public_post_link(None)
        assert username is None
        assert post_id is None

    def test_username_with_underscores_and_digits(self):
        username, post_id = extract_public_post_link("https://t.me/My_Channel_99/100")
        assert username == "My_Channel_99"
        assert post_id == 100


class TestDedupeCommentsByUser:
    def test_no_duplicates(self):
        comments = [
            {"sender_id": 1, "text": "a", "username": "u1", "name": "N1"},
            {"sender_id": 2, "text": "b", "username": "u2", "name": "N2"},
        ]
        result = dedupe_comments_by_user(comments)
        assert len(result) == 2

    def test_removes_duplicates(self):
        comments = [
            {"sender_id": 1, "text": "first", "username": "u1", "name": "N1"},
            {"sender_id": 1, "text": "second", "username": "u1", "name": "N1"},
            {"sender_id": 2, "text": "third", "username": "u2", "name": "N2"},
        ]
        result = dedupe_comments_by_user(comments)
        assert len(result) == 2
        assert result[0]["text"] == "first"
        assert result[1]["text"] == "third"

    def test_keeps_first_occurrence(self):
        comments = [
            {"sender_id": 5, "text": "keep me", "username": "u5", "name": "N5"},
            {"sender_id": 5, "text": "discard me", "username": "u5", "name": "N5"},
        ]
        result = dedupe_comments_by_user(comments)
        assert len(result) == 1
        assert result[0]["text"] == "keep me"

    def test_empty_list(self):
        assert dedupe_comments_by_user([]) == []
