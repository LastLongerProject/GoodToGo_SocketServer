from package.Api.JWT import Jwt, jwt
from package.Util import randHex
import requests
import time
from enum import Enum

"""
API document: https://doc.goodtogo.tw/#api-Containers-Containers_rent_container
You can look up all the meaning of status code with the corresponding endpoints in document
"""

baseUrl = "https://app.goodtogo.tw/"


class Uri:
    login = "/users/login"
    userToken = "/stores/getUser/"
    socketToken = "/containers/challenge/token"
    returnContainer = "/containers/return/"
    lendContainer = "/containers/rent/"
    usedAmount = "/stores/usedAmount"
    reloadContainer = "/containers/readyToClean/"
    createStockBox = "/deliveryList/stock"
    modifyDeliveryBoxInfo = "/deliveryList/modifyBoxInfo/"
    signDeliveryBox = "/deliveryList/sign"
    modifyDeliveryBoxState = "/deliveryList/changeState"


class ContainerActionReply(Enum):
    SUCCESS = 1
    CONTAINER_NOT_FOUND = "F002"
    CONTAINER_NOT_AVAILABLE = "F003"
    CONTAINER_STATE_ERROR = "H007"
    UNKNOWN_ERROR = "999"


class Api:
    def __init__(self):
        self.ver = "/v7"
        self.apiKey = "apiKey"
        self.secretKey = "secretKey"

    def setAuthorization(self, apiKey, secretKey):
        """
        Description   - set the authorization info
        Parameters    - api key(string)
                        secret key(string)
        Return values - N/A
        """
        self.apiKey = apiKey
        self.secretKey = secretKey

    def setVersion(self, version):
        """
        Description   - set the api version
        Parameters    - version(string)
        Return values - N/A
        """
        self.ver = version

    def login(self, username, password):
        """
        This api is no longer need to be called since it's using a bot account currently.
        """
        headers = {"reqID": randHex(10), "reqTime": str(time.time() * 1000)}
        body = {"phone": username, "password": password}
        r = requests.post(baseUrl + self.ver + Uri.login, data=body, headers=headers)
        encoded = r.headers["Authorization"]
        payload = jwt.decode(encoded, algorithms=["HS256"], verify=False)
        self.secretKey = payload["roles"]["clerk"]["secretKey"]
        self.apiKey = payload["roles"]["clerk"]["apiKey"]
        return (self.apiKey, self.secretKey)

    def fetchSocketNamespaceAndToken(self):
        """
        Description   - Fetch crucial information used for connecting to server websocket
        Parameters    - N/A
        Retrun values - status code(number),
                        token(string)
                        real uri(string)
        """
        headers = {"Authorization": Jwt.standard(self.secretKey), "apiKey": self.apiKey}
        r = requests.get(baseUrl + self.ver + Uri.socketToken, headers=headers)
        json = r.json()
        (token, uri) = (json["token"], json["uri"])
        return (r.status_code, token, uri)

    def reloadContainer(self, id):
        """
        Description   - Mark a container as clean after used
        Parameters    - id: containerId
                        date: timestamps of the action
        Return values - status code(number)
        """
        if not isinstance(id, list):
            id = [id]
        headers = {
            "Authorization": Jwt.addDate(self.secretKey),
            "apiKey": self.apiKey,
            "Content-Type": "application/json",
        }
        try:
            r = requests.post(
                baseUrl + self.ver + Uri.reloadContainer + "list",
                headers=headers,
                json={"containers": id},
            )
        except EnvironmentError as error:
            print(error)
            return None
        if r.status_code == 200:
            return ContainerActionReply.SUCCESS
        elif r.status_code == 403:
            if ContainerActionReply(r.json()["code"]):
                return ContainerActionReply(r.json()["code"])
            else:
                return ContainerActionReply.UNKNOWN_ERROR
        else:
            return ContainerActionReply.UNKNOWN_ERROR

    def returnContainer(self, id):
        """
        Description   - Mark a container as taken back from an user
        Parameters    - id: containerId
        Return values - status code(number)
                        previous host(string)
                        container id(string)
                        container type(string)
        """
        if not isinstance(id, list):
            id = [id]
        headers = {
            "Authorization": Jwt.addDate(self.secretKey),
            "apiKey": self.apiKey,
            "Content-Type": "application/json",
        }
        try:
            r = requests.post(
                baseUrl + self.ver + Uri.returnContainer + "list",
                headers=headers,
                json={"containers": id},
            )
        except EnvironmentError as error:
            print(error)
            return None
        if r.status_code == 200:
            return ContainerActionReply.SUCCESS
        elif r.status_code == 403:
            if ContainerActionReply(r.json()["code"]):
                return ContainerActionReply(r.json()["code"])
            else:
                return ContainerActionReply.UNKNOWN_ERROR
        else:
            return ContainerActionReply.UNKNOWN_ERROR

    def rentContainer(self, id, userApiKey):
        """
        Description   - Rent a container to an user
        Parameters    - id: container id
                        userApiKey: the apiKey of the user, you can get it by calling `fetchUserToken(self, user)`
        Return values - status code(number)
        """
        headers = {
            "Authorization": Jwt.addDate(self.secretKey),
            "apiKey": self.apiKey,
            "userApiKey": userApiKey,
        }
        r = requests.post(
            baseUrl + self.ver + Uri.lendContainer + str(id), headers=headers
        )
        return r.status_code

    def createDeliveryStockBox(self, ids):
        """
        Descriptions    - Create a stocked delivery box
        Parameters      - ids: id of containers for stocking
        Return values   - status code(number)
        """
        headers = {
            "Authorization": Jwt.standard(self.secretKey),
            "apiKey": self.apiKey,
            "Content-Type": "application/json",
        }
        r = requests.post(
            baseUrl + self.ver + Uri.createStockBox,
            headers=headers,
            json={"phone": "", "boxList": [{"boxName": "", "containerList": ids}]},
        )
        return r.status_code

    def modifyDeliveryBoxDestination(self, boxId, storeId):
        """
        Description    - modify destination of the box
        Parameters     - boxId: the id of the target box
                         storeId: new destination
        Return values  - status code(number)
        """
        return self.modifyDeliveryBoxInfo(boxId, {"storeID": storeId})

    def modifyDeliveryBoxInfo(self, boxId, body):
        """
        Description    - modify info of the box
        Parameters     - boxId: the id of the target box
                         body: new info
        Return values  - status code(number)
        """
        headers = {
            "Authorization": Jwt.standard(self.secretKey),
            "apiKey": self.apiKey,
            "Content-Type": "application/json",
        }
        r = requests.post(
            baseUrl + self.ver + Uri.modifyDeliveryBoxInfo + str(boxId),
            headers=headers,
            json=body,
        )
        return r.status_code

    def modifyDeliveryBoxState(self, boxId, newState):
        """
        Description     - modify state of the box
        Parameters      - boxId: the id of the box
                          newState: the new state of the box
        Return values   - status code(number)
        """
        headers = {
            "Authorization": Jwt.standard(self.secretKey),
            "apiKey": self.apiKey,
            "Content-Type": "application/json",
        }
        r = requests.post(
            baseUrl + self.ver + Uri.modifyDeliveryBoxState,
            headers=headers,
            json={"phone": "", "boxList": [{"id": str(boxId), "newState": newState}]},
        )
        return r.status_code

    def signDeliveryBox(self, boxId):
        """
        Description   - sign the =box
        Parameters    - boxId: target box
        Return values - status code(number)
        """
        headers = {
            "Authorization": Jwt.standard(self.secretKey),
            "apiKey": self.apiKey,
            "Content-Type": "application/json",
        }
        r = requests.post(
            baseUrl + self.ver + Uri.signDeliveryBox,
            headers=headers,
            json={"phone": "", "boxList": [{"ID": str(boxId)}]},
        )
        return r.status_code

    def fetchUserToken(self, user):
        """
        Description   - fetch the apiKey of a specific user
        Parameters    - user: phone number of the user
        Return values - status code(number)
                        api key(string)
        """
        headers = {"Authorization": Jwt.standard(self.secretKey), "apiKey": self.apiKey}
        r = requests.get(baseUrl + self.ver + Uri.userToken + user, headers=headers)
        if r.status_code == 200:
            json = r.json()
            return (r.status_code, json["apiKey"])
        else:
            return (r.status_code, "")

    def usedAmount(self):
        """
        Description   - get used amount of this bot
        Parameters    - N/A
        Return values - status code(number)
                        total amount of used containers(number)
        """
        headers = {"Authorization": Jwt.standard(self.secretKey), "apiKey": self.apiKey}
        r = requests.get(baseUrl + self.ver + Uri.usedAmount, headers=headers)
        json = r.json()
        print(json)
        storeRecords = json["store"]

        total = 0

        if r.status_code == 200:
            for record in storeRecords:
                total += record["amount"]
            return (r.status_code, total)
        else:
            return (r.status_code, 0)
