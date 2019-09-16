import requests
import pytest
import json
from collections import OrderedDict

class WorkerResult(object):
    NO_ERR = 0

    # Input parameters are illegal
    ERR_REV = 1

    # undefined ingredient in manifest
    ERR_INGREDIENT_UNDEFINED = 2

    # Unsupported ingredient in platform
    ERR_UNSUPPORTED_INGREDIENT_IN_PLATFORM = 3

    # Unsupported platform
    ERR_UNSUPPORTED_PLATFORM = 4

    # Unsupported attribute on specified element
    ERR_UNSUPPORTED_ATTRIBUTE = 5

    # NO ingredient media on ATF
    ERR_NONEXISTENT_MEDIA = 6

    # No change happened
    ERR_NO_CHANGE = 7

    # Input format error
    ERR_INPUT_FORMAT = 8

    # Git command err
    ERR_GIT_COMMAND = 9

    # other exception errors
    ERR_UNKNOWN = 999

    def __init__(self, err_code, content):
        self.code = err_code
        self.content = content


class TestPowrApi(object):
    """ """
    domain = "http://10.239.52.24:5000"
    data = json.loads(open('powrdata.json', 'r').read(), object_pairs_hook=OrderedDict)

    payload_manifest_revision = data["manifest_revision"]
    payload_get_project = data["get_project"]
    payload_get_ingredient_supported_platforms = data["get_ingredient_supported_platforms"]
    payload_get_platforms = data["get_platforms"]
    payload_get_platform = data["get_platform"]
    payload_patch_ingredients= data["patch_ingredients"]
    payload_patch_ingredient_supported_platforms = data["patch_ingredient_supported_platforms"]
    payload_patch_platform_images = data["patch_platform_images"]
    payload_patch_platform_ingredient = data["patch_platform_ingredient"]


    @classmethod
    def ret_code_assert(cls, ret_code, res):
        if ret_code == WorkerResult.NO_ERR:
            assert res.status_code == 200
        if ret_code == WorkerResult.ERR_REV:
            assert res.status_code == 404
            assert res.json()["errors"][0]["code"] == WorkerResult.ERR_REV
        if ret_code == WorkerResult.ERR_INGREDIENT_UNDEFINED:
            assert res.status_code == 404
            assert res.json()["errors"][0]["code"] == WorkerResult.ERR_INGREDIENT_UNDEFINED
        if ret_code == WorkerResult.ERR_UNSUPPORTED_INGREDIENT_IN_PLATFORM:
            assert res.status_code == 404
            assert res.json()["errors"][0]["code"] == WorkerResult.ERR_UNSUPPORTED_INGREDIENT_IN_PLATFORM
        if ret_code == WorkerResult.ERR_UNSUPPORTED_PLATFORM:
            assert res.status_code == 404
            assert res.json()["errors"][0]["code"] == WorkerResult.ERR_UNSUPPORTED_PLATFORM
        if ret_code == WorkerResult.ERR_UNSUPPORTED_ATTRIBUTE:
            assert res.status_code == 404
            assert res.json()["errors"][0]["code"] == WorkerResult.ERR_UNSUPPORTED_ATTRIBUTE
        if ret_code == WorkerResult.ERR_NONEXISTENT_MEDIA:
            assert res.status_code == 404
            assert res.json()["errors"][0]["code"] == WorkerResult.ERR_NONEXISTENT_MEDIA
        if ret_code == WorkerResult.ERR_NO_CHANGE:
            assert res.status_code == 404
            assert res.json()["errors"][0]["code"] == WorkerResult.ERR_NO_CHANGE
        if ret_code == WorkerResult.ERR_INPUT_FORMAT:
            assert res.status_code == 404
            assert res.json()["errors"][0]["code"] == WorkerResult.ERR_INPUT_FORMAT
        if ret_code == WorkerResult.ERR_GIT_COMMAND:
            assert res.status_code == 404
            assert res.json()["errors"][0]["code"] == WorkerResult.ERR_GIT_COMMAND
        if ret_code == WorkerResult.ERR_UNKNOWN:
            assert res.status_code == 404
            assert res.json()["errors"][0]["code"] == WorkerResult.ERR_UNKNOWN

    # [GET] "apidocs"
    def test_apidocs(self,):
        path = '/apidocs'
        url = self.domain + path
        res = requests.get(url, stream=True)
        assert res.status_code == 200

    # [GET] "/"
    def test_root(self):
        path = '/api/0/rev/HEAD/manifest/ingredients'
        url = self.domain + path
        res = requests.get(url, stream=True)
        assert res.status_code == 200

    # [GET] "/api/0/rev/"
    def test_revs(self):
        path = "/api/0/rev/"
        url = self.domain + path
        res = requests.get(url, stream=True)
        assert res.status_code == 200

    # [GET] "/api/0/rev/<path:rev>/manifest/ingredients"
    @pytest.mark.parametrize('payload', payload_manifest_revision)
    def test_manifest_revision(self, payload):
        rev, locator, ret_code = payload.values()
        path = "/api/0/rev/{}/manifest/ingredients{}".format(rev, locator)
        url = self.domain + path
        res = requests.get(url)
        self.ret_code_assert(ret_code, res)

    # [GET] "/api/0/rev/<path:rev>/manifest/ingredients/<ingredient>"
    @pytest.mark.parametrize('payload', payload_get_project)
    def test_get_project(self, payload):
        rev, ingredient, platform, ret_code = payload.values()
        path = "/api/0/rev/{}/manifest/ingredients/{}{}".format(rev,ingredient,platform)
        url = self.domain + path
        res = requests.get(url)
        self.ret_code_assert(ret_code, res)

    # [GET] "/api/0/rev/<path:rev>/manifest/<ingredient>/platforms"
    @pytest.mark.parametrize('payload', payload_get_ingredient_supported_platforms)
    def test_get_ingredient_supported_platforms(self,payload):
        rev, ingredient, ret_code = payload.values()
        path = "/api/0/rev/{}/manifest/{}/platforms".format(rev, ingredient)
        url = self.domain + path
        res = requests.get(url)
        self.ret_code_assert(ret_code, res)

    # [GAT] "/api/0/rev/<path:rev>/platforms"
    @pytest.mark.parametrize('payload', payload_get_platforms)
    def test_get_platforms(self, payload):
        rev, ret_code = payload.values()
        path = "/api/0/rev/{}/platforms".format(rev)
        url = self.domain + path
        res = requests.get(url)
        self.ret_code_assert(ret_code, res)

    # [GAT] "/api/0/rev/<path:rev>/platforms/<platform>"
    @pytest.mark.parametrize('payload', payload_get_platform)
    def test_get_platform(self, payload):
        rev, platform, ret_code = payload.values()
        path = "/api/0/rev/{}/platforms/{}".format(rev, platform)
        url = self.domain + path
        res = requests.get(url)
        self.ret_code_assert(ret_code, res)

    # [GAT] "/api/0/rev/<path:rev>/platforms/<platform>/image"
    @pytest.mark.parametrize('payload', payload_get_platform)
    def test_get_platform_images(self, payload):
        rev, platform, ret_code = payload.values()
        path = "/api/0/rev/{}/platforms/{}/image".format(rev, platform)
        url = self.domain + path
        res = requests.get(url)
        self.ret_code_assert(ret_code, res)

    # [GAT] "/api/0/rev/<path:rev>/platforms/<platform>/ingredients"
    @pytest.mark.parametrize('payload', payload_get_platform)
    def test_get_platform_ingredients(self, payload):
        rev, platform, ret_code = payload.values()
        path = "/api/0/rev/{}/platforms/{}/ingredients".format(rev, platform)
        url = self.domain + path
        res = requests.get(url)
        self.ret_code_assert(ret_code, res)

    # [PATCH] "/api/0/rev/<path:rev>/manifest/ingredients"
    @pytest.mark.parametrize('payload', payload_patch_ingredients)
    def test_patch_ingredients(self, payload):
        ret_code, rev, headers, data = payload.values()
        path = "/api/0/rev/{}/manifest/ingredients".format(rev)
        url = self.domain + path
        res = requests.patch(url, headers=headers, json=data)
        self.ret_code_assert(ret_code, res)

    # [PATCH] "/api/0/rev/<path:rev>/manifest/<ingredient>/platforms/<platform>"
    @pytest.mark.parametrize('payload', payload_patch_ingredient_supported_platforms)
    def test_patch_ingredient_supported_platforms(self, payload):
        ret_code, rev, ingredient, platform, headers, data = payload.values()
        path = "/api/0/rev/{}/manifest/{}/platforms/{}".format(rev ,ingredient, platform)
        url = self.domain + path
        res = requests.patch(url, headers=headers, json=data)
        self.ret_code_assert(ret_code, res)

    # [PATCH] "/api/0/rev/<path:rev>/platforms/<platform>/image"
    @pytest.mark.parametrize('payload', payload_patch_platform_images)
    def test_patch_platform_images(self, payload):
        ret_code, rev, platform, headers, data = payload.values()
        path = "/api/0/rev/{}/platforms/{}/image".format(rev, platform)
        url = self.domain + path
        res = requests.patch(url, headers=headers, json=data)
        self.ret_code_assert(ret_code, res)

    # [PATCH] "/api/0/rev/<path:rev>/platforms/<platform>/ingredients"
    @pytest.mark.parametrize('payload', payload_patch_platform_ingredient)
    def test_patch_platform_ingredient(self, payload):
        ret_code, rev, platform, headers, data = payload.values()
        path = "/api/0/rev/{}/platforms/{}/ingredients".format(rev, platform)
        url = self.domain + path
        res = requests.patch(url, headers=headers, json=data)
        self.ret_code_assert(ret_code, res)
