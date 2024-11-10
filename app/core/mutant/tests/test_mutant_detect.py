# core/mutant/tests/test_mutant_endpoint.py

import pytest
from adapters.database.models import DNA
from conftest import app
from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm.session import Session


class TestMutantDetection:
    """
    Clase para probar el endpoint de detección de mutantes.
    """

    @pytest.fixture(autouse=True)
    def initialize(self, db_session: Session) -> None:
        """
        Fixture that initializes the test environment.

        This fixture is used to set up the test environment before each test case is executed.
        It creates a TestClient object for making HTTP requests to the application and initializes the database session.

        Args:
            db_session (Session): The database session object.
        """
        self.client = TestClient(app)
        self.db_session: Session = db_session

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """
        Configura el entorno de prueba.
        """
        self.url = "/api/v1/mutant/"

    def test_detect_mutant_horizontal(self) -> None:
        """
        Prueba de detección de mutante con secuencia horizontal.
        """
        dna_sequence = ["AAAA", "CAGT", "TTTT", "AGAG"]
        concatenated_sequence = "".join(dna_sequence)
        response: Response = self.client.post(self.url, json={"dna": dna_sequence})
        db_record = (
            self.db_session.query(DNA).filter_by(sequence=concatenated_sequence).first()
        )
        assert db_record is not None
        assert response.status_code == 200
        assert response.json() == {"message": "Mutant detected"}

    def test_detect_mutant_vertical(self) -> None:
        """
        Prueba de detección de mutante con secuencia vertical.
        """
        dna_sequence = ["ATGC", "ATGC", "ATGC", "ATGC"]

        response: Response = self.client.post(self.url, json={"dna": dna_sequence})
        db_record = (
            self.db_session.query(DNA).filter_by(sequence="".join(dna_sequence)).first()
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Mutant detected"}

    def test_detect_mutant_diagonal(self) -> None:
        """
        Prueba de detección de mutante con secuencia diagonal.
        """
        response: Response = self.client.post(
            self.url,
            json={"dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]},
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Mutant detected"}

    def test_detect_not_mutant(self) -> None:
        """
        Prueba de detección de no mutante.
        """
        response: Response = self.client.post(
            self.url,
            json={"dna": ["ACGCGA", "CTGTGC", "TTATGT", "AGAAGG", "CCTATA", "TCACTG"]},
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "Not a mutant"}

    def test_invalid_dna_format(self) -> None:
        """
        Prueba de error por formato de ADN no válido.
        """
        response = self.client.post(
            self.url,
            json={"dna": ["ACGC", "CTGTGC", "TTATGT", "AGAAGG", "CCTATA", "TCACTG"]},
        )
        response_data = response.json()
        assert response.status_code == 422
        assert "msg" in response_data["detail"][0]
        assert (
            response_data["detail"][0]["msg"]
            == "Value error, Each DNA string must have the same length"
        )
        assert response_data["detail"][0]["type"] == "value_error"
