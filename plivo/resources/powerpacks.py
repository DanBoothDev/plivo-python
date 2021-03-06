# -*- coding: utf-8 -*-
from plivo.utils.validators import *

from ..base import ListResponseObject, PlivoResource, PlivoResourceInterface, ResponseObject
from ..exceptions import *
from ..utils import *
from plivo.resources.numberpools import NumberPool

class Powerpack(PlivoResource):
    _name = 'Powerpack'
    _identifier_string = 'uuid'
    numberpool = None

    def get(self):
        return self.client.powerpacks.get(self.id)

    def delete(self, unrent_numbers=False):
        params ={}
        params['unrent_numbers'] = unrent_numbers
        return self.client.request('DELETE', ('Powerpack', self.id),
                                    params,  response_type=None,objects_type=None)
    # params values should be dictionary like {'sticky_sender': false, 'name':"hello"} 
    def update(self,params=None):
        if params == None:
            raise ValidationError(
                'required atleast one of powerpack attributes'
            )
        return self.client.request('POST', ('Powerpack', self.id),
                                   params, response_type=None,
                objects_type=None)

    def get_numberpooluuid(self):
        powerpack = self.client.request(
            'GET', ('Powerpack', self.id), response_type=Powerpack)
        numberpoolpath = powerpack.number_pool
        numberpool_uuid = ""
        if numberpoolpath:
            numberpool = numberpoolpath.split('/')
            numberpool_uuid = numberpool[5]
            return numberpool_uuid
        return ""

    @validate_args(
        limit=[
            optional(
                all_of(
                    of_type(*six.integer_types),
                    check(lambda limit: 0 < limit <= 20, '0 < limit <= 20')))
        ],
        offset=[
            optional(
                all_of(
                    of_type(*six.integer_types),
                    check(lambda offset: 0 <= offset, '0 <= offset')))
        ])
        

    def list_numbers(self,
        starts_with=None, 
        country_iso2=None,
        type=None, limit=None, offset=None):
        numberpool_uuid = self.get_numberpooluuid()
        params ={}
        if starts_with:
            params['starts_with'] = starts_with
        if country_iso2:
            params['country_iso2'] = country_iso2
        if type:
            params['type'] = type
        if limit:
            params['limit']= limit
        if offset:
            params['offset'] = offset
        if numberpool_uuid != "":
            return self.client.request('GET', ('NumberPool',numberpool_uuid,'Number'),
                params ,response_type=None,
                objects_type=None)
        else:
            raise ResourceNotFoundError('Resource not found')

    def count_numbers(self,
        starts_with=None, 
        country_iso2=None,
        type=None):
        numberpool_uuid = self.get_numberpooluuid()
        params ={}
        if starts_with:
            params['starts_with'] = starts_with
        if country_iso2:
            params['country_iso2'] = country_iso2
        if type:
            params['type'] = type
        if numberpool_uuid != "":
            try:
                response = self.client.request(
                'GET', ('NumberPool',numberpool_uuid,'Number'),
                params ,response_type=None,
                objects_type=None)
                return response['meta']['total_count']
            except:
                return 0
        else:
            raise ResourceNotFoundError('Resource not found')


    @validate_args(
    number=[of_type(six.text_type)]
    )
    def find_number(self, number):
        numberpool_uuid = self.get_numberpooluuid()
        if numberpool_uuid != "":
            return self.client.request(
            'GET', ('NumberPool',numberpool_uuid,'Number', number),
            response_type=None,
            objects_type=None)
        else:
            raise ResourceNotFoundError('Resource not found')

    @validate_args(
    number=[of_type(six.text_type)]
    )
    def add_number(self,  number):
        numberpool_uuid = self.get_numberpooluuid()
        if numberpool_uuid != "":
            return self.client.request(
            'POST', ('NumberPool',numberpool_uuid,'Number', number),
            response_type=None,
            objects_type=Powerpack)
        else:
            raise ResourceNotFoundError('Resource not found')

    @validate_args(
    number=[of_type(six.text_type)]
    )
    def remove_number(self,  number, unrent=False):
        numberpool_uuid = self.get_numberpooluuid()
        params = {}
        params['unrent'] = unrent
        if numberpool_uuid != "":
            return self.client.request(
            'DELETE', ('NumberPool',numberpool_uuid,'Number', number), params,
            response_type=None,
            objects_type=None)
        else:
            raise ResourceNotFoundError('Resource not found')


    @validate_args(
        limit=[
            optional(
                all_of(
                    of_type(*six.integer_types),
                    check(lambda limit: 0 < limit <= 20, '0 < limit <= 20')))
        ],
        offset=[
            optional(
                all_of(
                    of_type(*six.integer_types),
                    check(lambda offset: 0 <= offset, '0 <= offset')))
        ])
    def list_shortcodes(self,  limit=20, offset=0):
        params ={}
        params['limit'] = limit
        params['offset'] = offset
        numberpool_uuid = self.get_numberpooluuid()
        if numberpool_uuid != "":
            return self.client.request(
            'GET', ('NumberPool',numberpool_uuid,'Shortcode'),
            params,
            response_type=None,
            objects_type=None)
        else:
            raise ResourceNotFoundError('Resource not found')

    @validate_args(
        shortcode=[of_type(six.text_type)])
    def find_shortcode(self,  shortcode):
        numberpool_uuid = self.get_numberpooluuid()
        if numberpool_uuid != "":
            return self.client.request(
            'GET', ('NumberPool',numberpool_uuid,'Shortcode', shortcode),
            response_type=None,
            objects_type=None)
        else:
            raise ResourceNotFoundError('Resource not found')



    def buy_add_number(self,
        pattern=None,
        country_iso2=None,
        type=None, 
        region=None, 
        number=''):
        numberpool_uuid = self.get_numberpooluuid()
        params = {}
        params['rent'] = 'true'
        if numberpool_uuid != "":   
            if number !="":
                return self.client.request(
                'POST', ('NumberPool',numberpool_uuid,'Number', number),params,
                response_type=None,
                objects_type=None)
            else :
                phonenumberparam = {}
                if pattern:
                    phonenumberparam['pattern'] = pattern
                if type:
                    phonenumberparam['type'] = type
                if country_iso2:
                    phonenumberparam['country_iso'] = country_iso2
                if region:
                    phonenumberparam['region'] = region
                number_response = self.client.request(
                        'GET',
                        ('PhoneNumber', ),
                        phonenumberparam,
                        objects_type=None,
                        response_type=None, )
                if len(number_response)< 1:
                    raise  ResourceNotFoundError('Resource not found')
                number = number_response[0]['number']
                return self.client.request(
                'POST', ('NumberPool',numberpool_uuid,'Number', number),params,
                response_type=None,
                objects_type=None)
        else:
            raise ResourceNotFoundError('Resource not found')
     
    
class Powerpacks(PlivoResourceInterface):
    _resource_type = Powerpack
    @validate_args(
        sticky_sender=[optional(of_type_exact(bool))],
        local_connect=[optional(of_type_exact(bool))],
        application_type=[optional(of_type(six.text_type))],
        application_id=[optional(of_type(six.text_type))])
    def create(self,
               name,
               sticky_sender=True,
               local_connect=True,
               application_type='',
               application_id=''):
        if (name is None):
            raise ValidationError(
                'name parameter is invalid'
            )
        return self.client.request('POST', ('Powerpack', ),
                                   to_param_dict(self.create, locals()))
    
    @validate_args(uuid=[of_type(six.text_type)])
    def get(self, uuid):
        response = self.client.request(
            'GET', ('Powerpack', uuid), response_type=Powerpack)
        numberpoolpath = response.number_pool
        number_pool_id = ""
        if numberpoolpath:
            numberpool = numberpoolpath.split('/')
            number_pool_id = numberpool[5]
            data = {
            'number_pool_id': number_pool_id
        }
            Powerpack.numberpool = NumberPool( self.client, data)
        return response

    @validate_args(
        limit=[
            optional(
                all_of(
                    of_type(*six.integer_types),
                    check(lambda limit: 0 < limit <= 20, '0 < limit <= 20')))
        ],
        offset=[
            optional(
                all_of(
                    of_type(*six.integer_types),
                    check(lambda offset: 0 <= offset, '0 <= offset')))
        ])
    def list(self,
             limit=None,
             offset=None):
        return self.client.request(
            'GET', ('Powerpack', ),
            to_param_dict(self.list, locals()),
            response_type=None,
            objects_type=None)
 
    
