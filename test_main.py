from fastapi.testclient import TestClient
from main import app


#Import test client
client = TestClient(app)

#Test to test the update wms coordinate file function
def test_update_wms_coordinate_file():
    response = client.post(
        "/updateWMSCoordinateFile",
        headers = {'Content-Type': 'application/json'},
        json={"input": [1,2,4,4]}
    )

    #Check that the responses are okay
    assert response.status_code == 200
    assert response.json() == {"Message": "Coordinates were updated successfully"}



    
