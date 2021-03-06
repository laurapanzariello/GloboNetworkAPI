# -*- coding: utf-8 -*-
import logging

from django.test.client import Client
from mock import patch

from networkapi.api_vip_request.models import VipRequest
from networkapi.api_vip_request.serializers.v3 import VipRequestV3Serializer
from networkapi.api_vip_request.tasks.deploy import undeploy
from networkapi.test.test_case import NetworkApiTestCase
from networkapi.usuario.models import Usuario

log = logging.getLogger(__name__)


class VipRequestAsyncDeleteDeploySuccessTestCase(NetworkApiTestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    @patch('networkapi.api_vip_request.facade.v3.delete_real_vip_request')
    @patch('networkapi.api_vip_request.facade.v3.get_vip_request_by_id')
    @patch('networkapi.usuario.models.Usuario.objects.get')
    @patch('networkapi.api_vip_request.tasks.deploy.undeploy.update_state')
    def test_task_id_create_in_delete_deploy_one_vip_request_success(self, *args):
        """Test success of id task generate for vip request delete deploy success."""
        mock_get_user = args[1]
        mock_get_vip = args[2]
        mock_delete_real_vip = args[3]

        user = Usuario(id=1, nome='test')

        vip = VipRequest(id=1)
        vip_serializer = VipRequestV3Serializer(
            vip, include=('ports__identifier',))

        mock_delete_real_vip.return_value = vip
        mock_get_vip.return_value = vip
        mock_get_user.return_value = user

        undeploy(vip.id, user.id)

        mock_delete_real_vip.assert_called_with(
            [vip_serializer.data], user)
