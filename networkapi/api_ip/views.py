# -*- coding: utf-8 -*-
import logging

from django.db.transaction import commit_on_success
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from networkapi.api_ip import facade
from networkapi.api_ip import serializers
from networkapi.api_ip.permissions import Read
from networkapi.api_ip.permissions import Write
from networkapi.api_rest import exceptions as api_exceptions
from networkapi.settings import SPECS
from networkapi.util.classes import CustomAPIView
from networkapi.util.decorators import logs_method_apiview
from networkapi.util.decorators import permission_classes_apiview
from networkapi.util.decorators import prepare_search
from networkapi.util.geral import render_to_json
from networkapi.util.json_validate import json_validate
from networkapi.util.json_validate import raise_json_validate

log = logging.getLogger(__name__)


class IPv4View(CustomAPIView):

    @logs_method_apiview
    @raise_json_validate()
    @permission_classes_apiview((IsAuthenticated, Read))
    @prepare_search
    def get(self, request, *args, **kwargs):
        """Returns a list of vip request by ids ou dict."""

        if not kwargs.get('obj_id'):
            obj_model = facade.get_ipv4_by_search(self.search)
            ips = obj_model['query_set']
            only_main_property = False
        else:
            obj_ids = kwargs.get('obj_id').split(';')
            ips = facade.get_ipv4_by_ids(obj_ids)
            only_main_property = True
            obj_model = None

        # serializer ips
        serializer_ip = serializers.Ipv4V3Serializer(
            ips,
            many=True,
            fields=self.fields,
            include=self.include,
            exclude=self.exclude,
            kind=self.kind
        )

        # prepare serializer with customized properties
        data = render_to_json(
            serializer_ip,
            main_property='ips',
            obj_model=obj_model,
            request=request,
            only_main_property=only_main_property
        )

        return Response(data, status=status.HTTP_200_OK)

    @permission_classes_apiview((IsAuthenticated, Write))
    @logs_method_apiview
    @raise_json_validate('ipv4_post')
    @commit_on_success
    def post(self, request, *args, **kwargs):
        """Save Ipv4"""

        ips = request.DATA
        json_validate(SPECS.get('ipv4_post')).validate(ips)
        response = list()
        for ip in ips['ips']:
            ret = facade.create_ipv4(ip, request.user)
            response.append({'id': ret.id})

        return Response(response, status=status.HTTP_201_CREATED)

    @permission_classes_apiview((IsAuthenticated, Write))
    @logs_method_apiview
    @raise_json_validate('ipv4_put')
    @commit_on_success
    def put(self, request, *args, **kwargs):
        """Edit Ipv4"""

        ips = request.DATA
        json_validate(SPECS.get('ipv4_put')).validate(ips)
        response = list()
        for ip in ips['ips']:
            ret = facade.update_ipv4(ip, request.user)
            response.append({'id': ret.id})

        return Response(response, status=status.HTTP_200_OK)

    @permission_classes_apiview((IsAuthenticated, Write))
    @logs_method_apiview
    @raise_json_validate()
    @commit_on_success
    def delete(self, request, *args, **kwargs):
        """Edit Ipv4"""

        obj_ids = kwargs['obj_id'].split(';')
        facade.delete_ipv4_list(obj_ids)

        return Response({}, status=status.HTTP_200_OK)


class IPv6View(CustomAPIView):

    @logs_method_apiview
    @permission_classes_apiview((IsAuthenticated, Read))
    @prepare_search
    def get(self, request, *args, **kwargs):

        try:

            if not kwargs.get('obj_id'):
                obj_model = facade.get_ipv6_by_search(self.search)
                ips = obj_model['query_set']
                only_main_property = False
            else:
                obj_ids = kwargs.get('obj_id').split(';')
                ips = facade.get_ipv6_by_ids(obj_ids)
                only_main_property = True
                obj_model = None

            # serializer ips
            serializer_ip = serializers.Ipv6V3Serializer(
                ips,
                many=True,
                fields=self.fields,
                include=self.include,
                exclude=self.exclude,
                kind=self.kind
            )

            # prepare serializer with customized properties
            data = render_to_json(
                serializer_ip,
                main_property='ips',
                obj_model=obj_model,
                request=request,
                only_main_property=only_main_property
            )

            return Response(data, status=status.HTTP_200_OK)

        except Exception, exception:
            log.error(exception)
            raise api_exceptions.NetworkAPIException(exception)

    @permission_classes_apiview((IsAuthenticated, Write))
    @logs_method_apiview
    @raise_json_validate('ipv6_post')
    @commit_on_success
    def post(self, request, *args, **kwargs):
        """Save Ipv6."""

        ips = request.DATA
        json_validate(SPECS.get('ipv6_post')).validate(ips)
        response = list()
        for ip in ips['ips']:
            ret = facade.create_ipv6(ip, request.user)
            response.append({'id': ret.id})

        return Response(response, status=status.HTTP_201_CREATED)

    @permission_classes_apiview((IsAuthenticated, Write))
    @logs_method_apiview
    @raise_json_validate('ipv6_put')
    @commit_on_success
    def put(self, request, *args, **kwargs):
        """Edit Ipv6."""

        ips = request.DATA
        json_validate(SPECS.get('ipv6_put')).validate(ips)
        response = list()
        for ip in ips['ips']:
            ret = facade.update_ipv6(ip, request.user)
            response.append({'id': ret.id})

        return Response(response, status=status.HTTP_200_OK)

    @permission_classes_apiview((IsAuthenticated, Write))
    @logs_method_apiview
    @raise_json_validate()
    @commit_on_success
    def delete(self, request, *args, **kwargs):
        """Edit Ipv6"""

        obj_ids = kwargs['obj_id'].split(';')
        facade.delete_ipv6_list(obj_ids)

        return Response({}, status=status.HTTP_200_OK)
