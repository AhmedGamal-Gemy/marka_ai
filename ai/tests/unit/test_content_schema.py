import pytest
from pydantic import ValidationError
from app.schemas.content import ContentResponse


def test_content_response_valid():
    """Verify valid ContentResponse parses correctly with thought_process and 3 captions.

    Arrange: Create a dict with thought_process and a list of 3 Egyptian Arabic captions.
    Act: Instantiate ContentResponse with the valid data.
    Assert: All fields are populated and captions list has exactly 3 items.
    """
    # Arrange
    data = {
        "thought_process": "User wants marketing copy for a product. I will generate 3 captions.",
        "captions": [
            "جرب المنتج ده هيعجبك جداً!",
            "أحسن عرض هتلاقيه هنا عندنا",
            "اطلبه دلوقتي قبل ما يخلص!",
        ],
    }

    # Act
    response = ContentResponse(**data)

    # Assert
    assert response.thought_process == data["thought_process"]
    assert len(response.captions) == 3
    assert response.captions == data["captions"]


def test_content_response_captions_list():
    """Verify captions field is a list of strings.

    Arrange: Create a ContentResponse with a list of string captions.
    Act: Instantiate the model.
    Assert: captions is a list and every element is a str.
    """
    # Arrange
    data = {
        "thought_process": "Generating captions.",
        "captions": ["caption one", "caption two", "caption three"],
    }

    # Act
    response = ContentResponse(**data)

    # Assert
    assert isinstance(response.captions, list)
    assert all(isinstance(c, str) for c in response.captions)


def test_content_response_invalid_missing_field():
    """Verify ValidationError is raised when a required field is missing.

    Arrange: Create a dict missing the required 'captions' field.
    Act: Attempt to instantiate ContentResponse.
    Assert: pydantic.ValidationError is raised.
    """
    # Arrange
    incomplete_data = {
        "thought_process": "Some reasoning without captions.",
    }

    # Act & Assert
    with pytest.raises(ValidationError):
        ContentResponse(**incomplete_data)


def test_content_response_empty_captions():
    """Verify ContentResponse accepts an empty captions list as valid edge case.

    Arrange: Create a dict with an empty captions list.
    Act: Instantiate ContentResponse.
    Assert: Model parses successfully and captions is an empty list.
    """
    # Arrange
    data = {
        "thought_process": "No captions generated.",
        "captions": [],
    }

    # Act
    response = ContentResponse(**data)

    # Assert
    assert response.captions == []
    assert len(response.captions) == 0


def test_content_response_single_caption():
    """Verify ContentResponse parses correctly with a single caption.

    Arrange: Create a dict with thought_process and exactly 1 caption.
    Act: Instantiate ContentResponse.
    Assert: Model parses successfully and captions list has 1 item.
    """
    # Arrange
    data = {
        "thought_process": "User asked for just one caption.",
        "captions": ["منتج ممتاز بسعر حلو"],
    }

    # Act
    response = ContentResponse(**data)

    # Assert
    assert len(response.captions) == 1
    assert response.captions[0] == "منتج ممتاز بسعر حلو"
