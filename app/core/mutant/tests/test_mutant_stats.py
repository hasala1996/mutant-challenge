import pytest
from conftest import app
from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm import Session

from app.adapters.database.models import DNA


class TestStatsEndpoint:
    """
    Class to test the statistics endpoint (/stats/).
    """

    @pytest.fixture(autouse=True)
    def initialize(self, db_session: Session) -> None:
        """
        Fixture that initializes the test environment.

         Args:
             db_session (Session):The database session for testing.
        """
        self.client = TestClient(app)
        self.db_session = db_session

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """
        Set up the test environment.
        """
        self.url = "/api/v1/stats/"

    def create_mutant_humans(self) -> None:
        """
        Fill the database with 2 mutant and 2 non-mutant DNA sequences.
        """
        mutant_sequences = [
            "AAAACCCCAGTTTGGG",
            "TTTTGCCCAGTCAAGG",
        ]

        non_mutant_sequences = [
            "ATCGATCGATCGATCG",
            "CGTACGTACGTACGTA",
        ]

        for sequence in mutant_sequences:
            dna_record = DNA(sequence=sequence, is_mutant=True)
            self.db_session.add(dna_record)

        for sequence in non_mutant_sequences:
            dna_record = DNA(sequence=sequence, is_mutant=False)
            self.db_session.add(dna_record)

        self.db_session.commit()

    def test_stats_endpoint_no_data(self) -> None:
        """
        Test the statistics endpoint with no data in the database.
        """
        response: Response = self.client.get(self.url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["count_mutant_dna"] == 0
        assert response_data["count_human_dna"] == 0
        assert response_data["ratio"] == 0

    def test_stats_endpoint_with_data(self) -> None:
        """
        Test the statistics endpoint with 2 mutant and 2 non-mutant DNA sequences.
        """
        self.create_mutant_humans()

        response: Response = self.client.get(self.url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["count_mutant_dna"] == 2
        assert response_data["count_human_dna"] == 2
        assert response_data["ratio"] == 0.5

    def test_stats_endpoint_only_mutants(self) -> None:
        """
        Test the statistics endpoint with only mutant DNA sequences.
        """
        self.db_session.query(DNA).delete()
        self.db_session.commit()

        mutant_sequences = ["AAAACCCCAGTTTGGG", "TTTTGCCCAGTCAAGG"]
        for sequence in mutant_sequences:
            dna_record = DNA(sequence=sequence, is_mutant=True)
            self.db_session.add(dna_record)
        self.db_session.commit()

        response: Response = self.client.get(self.url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["count_mutant_dna"] == 2
        assert response_data["count_human_dna"] == 0
        assert response_data["ratio"] == 1

    def test_stats_endpoint_only_humans(self) -> None:
        """
        Test the statistics endpoint with only non-mutant DNA sequences.
        """
        self.db_session.query(DNA).delete()
        self.db_session.commit()

        non_mutant_sequences = ["ATCGATCGATCGATCG", "CGTACGTACGTACGTA"]
        for sequence in non_mutant_sequences:
            dna_record = DNA(sequence=sequence, is_mutant=False)
            self.db_session.add(dna_record)
        self.db_session.commit()

        response: Response = self.client.get(self.url)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["count_mutant_dna"] == 0
        assert response_data["count_human_dna"] == 2
        assert response_data["ratio"] == 0
