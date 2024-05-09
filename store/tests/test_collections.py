from rest_framework.test import APIClient
from rest_framework import status
import pytest

@pytest.mark.django_db
class TestCollection:
    def test_if_user_is_anonymous_returns_401(self):
        # Arrange
        
        
        # Act
        client=APIClient()
        response=client.post('store/collections/',{'title':'b'})
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND  