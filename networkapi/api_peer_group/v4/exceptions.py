# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.exceptions import APIException


class PeerGroupNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, msg):
        self.detail = u'PeerGroup id = {} do not exist'.format(msg)


class PeerGroupError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, msg):
        self.detail = msg


class EnvironmentPeerGroupNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, msg):
        self.detail = u'EnvironmentPeerGroup %s do not exist' % (msg)


class EnvironmentPeerGroupError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, msg):
        self.detail = msg


class PeerGroupDoesNotExistException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = u'PeerGroup does not exists'


class RouteMapInAndOutAreEqualException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        self.detail = u'RouteMapIn cant be equal RouteMapOut'


class EnvironmentPeerGroupDuplicatedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, env_peer_group):
        self.detail = u'Environment id = {} is already associated ' \
                      u'with Peer Group id = {}'. \
            format(env_peer_group.environment, env_peer_group.peer_group)


class PeerGroupDuplicatedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, peer_group):
        self.detail = u'Already exists PeerGroup with RouteMap id = {} ' \
                      u'or id = {}'.\
            format(peer_group.route_map_in, peer_group.route_map_out)


class PeerGroupIsAssociatedWithNeighborsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, peer_group):
        self.detail = u'PeerGroup id = {} is associated ' \
                      u'with NeighborsV4 id = {} and NeighborsV6 id = {}'.\
            format(peer_group.id,
                   peer_group.neighbors_v4_id, peer_group.neighbors_v6_id)


class PeerGroupAssociatedWithDeployedNeighborsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, peer_group):
        self.detail = u'PeerGroup id = {} is associated with deployed ' \
                      u'NeighborsV4 id = {} and NeighborsV6 id = {}'.\
            format(peer_group.id,
                   peer_group.neighbors_v4_id, peer_group.neighbors_v6_id)
