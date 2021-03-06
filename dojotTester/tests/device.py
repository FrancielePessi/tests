from tests.base_test import BaseTest
from dojot.api import DojotAPI as Api
import json
import random
import time


class DeviceTest(BaseTest):

    def createTemplates(self, jwt: str, templates: list):
        template_ids = []
        for template in templates:
            rc, template_id = Api.create_template(jwt, json.dumps(template))

            template_ids.append(template_id["template"]["id"]) if rc == 200 else template_ids.append(None)
        return template_ids


    def createDevices(self, jwt: str, devices: list):
        result = []

        for templates, label in devices:
            self.logger.info('adding device ' + label + ' using templates ' + str(templates))
            rc, res = Api.create_device(jwt, templates, label)
            #self.assertTrue(rc == 200, "Error on create device")
            device_id = None
            if rc == 200:
                device_id = res["devices"][0]["id"]
            result.append((rc, res, device_id))
        return result


    def createMultipleDevices(self, jwt: str, template_id: int, label: str, attrs: str):
        rc, res = Api.create_multiple_devices(jwt, template_id, label, attrs)

        # return rc, res if rc != 200 else res
        return res

    def updateDevice(self, jwt: str, device_id: int, template: str):
        rc, res = Api.update_device(jwt, device_id, json.dumps(template))
        # self.assertTrue(isinstance(device_id, int), "Error on update device")
        return res if rc == 200 else res

    def getDevices(self, jwt: str):
        rc, res = Api.get_all_devices(jwt)
        # self.assertTrue(isinstance(device_id, int), "Error on get devices")
        return res

    def getDevicesWithParameters(self, jwt: str, attrs: str):
        _, res = Api.get_devices_with_parameters(jwt, attrs)
        # self.assertTrue(isinstance(device_id, int), "Error on get devices")
        return res

    def getDevice(self, jwt: str, device_id: str):
        res = Api.get_single_device(jwt, device_id)
        # self.assertTrue(isinstance(device_id, int), "Error on get device")
        return res

    def deleteDevices(self, jwt: str):
        _, res = Api.delete_devices(jwt)
        # self.assertTrue(isinstance(device_id, int), "Error on delete template")
        return res

    def deleteDevice(self, jwt: str, device_id: int):
        res = Api.delete_device(jwt, device_id)
        # self.assertTrue(isinstance(device_id, int), "Error on delete template")
        return res

    def runTest(self):
        self.logger.info('Executing device test')
        self.logger.debug('getting jwt...')
        jwt = Api.get_jwt()

        self.logger.info('listing all devices...')
        res = self.getDevices(jwt)
        self.logger.debug(res)


        self.logger.info('creating template com todos os tipos de atributos...')

        templates = []
        self.logger.debug('creating templates...')
        templates.append({
            "label": "Template",
            "attrs": [
                {
                    "label": "float",
                    "type": "dynamic",
                    "value_type": "float"
                },
                {
                    "label": "int",
                    "type": "dynamic",
                    "value_type": "integer"
                },
                {
                    "label": "text",
                    "type": "dynamic",
                    "value_type": "string"
                },
                {
                    "label": "gps",
                    "type": "dynamic",
                    "value_type": "geo:point",
                    "metadata": [
                        {
                            "label": "descricao",
                            "type": "static",
                            "value_type": "string",
                            "static_value": "localizacao do device"
                        }
                    ]
                },
                {
                    "label": "bool",
                    "type": "dynamic",
                    "value_type": "bool"
                },
                {
                    "label": "mensagem",
                    "type": "actuator",
                    "value_type": "string"
                },
                {
                    "label": "serial",
                    "type": "static",
                    "value_type": "string",
                    "static_value": "indefinido"
                },
                {
                    "label": "objeto",
                    "type": "dynamic",
                    "value_type": "object"
                }
            ]
        })
        templates.append({
            "label": "SensorModel",
            "attrs": [
                {
                    "label": "temperature",
                    "type": "dynamic",
                    "value_type": "float"
                },
                {
                    "label": "model-id",
                    "type": "static",
                    "value_type": "string",
                    "static_value": "model-001"
                }
                ]
        })
        templates.append({
            "label": "Temperature",
            "attrs": [
                {
                    "label": "temperature",
                    "type": "dynamic",
                    "value_type": "float"
                }
                ]
        })

        template_ids = self.createTemplates(jwt, templates)
        self.logger.info("templates ids: " + str(template_ids))

        devices = []
        devices.append(([template_ids[0]], "dispositivo"))
        devices.append(([template_ids[1]], "sensor"))
        devices_ids = self.createDevices(jwt, devices)
        self.logger.info("devices ids: " + str(devices_ids))

        #TODO: 'listing device - by ID...'


        self.logger.info('listing device - by ID...')
        list = self.getDevice(jwt, Api.get_deviceid_by_label(jwt, 'dispositivo'))
        self.logger.debug('Device info: ' + str(list))


        """
          
        self.logger.debug('updating device ......')
        template = {
            "label": "dispositivo",
            "attrs": [
                {
                    "label": "serial",
                    "type": "static",
                    "value_type": "string",
                    "static_value": "0001"
                }
            ]
        }

        rc, res = self.updateDevice(jwt, device_id, template)
        self.logger.info('Device updated: ' + str(device_id))

        self.logger.info('listing updated template...')
        list = self.getDevice(jwt, device_id)
        self.logger.info('Device info: ' + str(list))
        """

        """
        Create multiple devices
        """

        self.logger.info('creating multiple devices...')
        device_list = self.createMultipleDevices(jwt, template_ids[1], 'test_device', "count=5")
        self.logger.info('Devices created: ' + str(device_list))

        self.logger.info('creating devices with verbose=False ...')
        device_list = self.createMultipleDevices(jwt, template_ids[1], 'test_verbose_false', "verbose=False")
        self.logger.debug('Device created: ' + str(device_list))

        self.logger.info('creating devices with verbose=True ...')
        device_list = self.createMultipleDevices(jwt, template_ids[1], 'test_verbose_true', "verbose=True")
        self.logger.debug('Device created: ' + str(device_list))

        """
        #Lista devices
        """

        self.logger.info('listing all devices...')
        list = self.getDevices(jwt)
        self.logger.debug('Device List: ' + str(list))

        self.logger.info('listing devices with parameter: page_size=4...')
        res = self.getDevicesWithParameters(jwt, "?page_size=4")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: page_num=2...')
        res = self.getDevicesWithParameters(jwt, "?page_num=2")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: page_size=3&page_num=1...')
        res = self.getDevicesWithParameters(jwt, "?page_size=3&page_num=1")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: page_size=3&page_num=2...')
        res = self.getDevicesWithParameters(jwt, "?page_size=3&page_num=2")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: page_size=3&page_num=3...')
        res = self.getDevicesWithParameters(jwt, "?page_size=3&page_num=3")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: page_size=3&page_num=4...')
        res = self.getDevicesWithParameters(jwt, "?page_size=3&page_num=4")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: idsOnly=true...')
        res = self.getDevicesWithParameters(jwt, "?idsOnly=true")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: idsOnly=false...')
        res = self.getDevicesWithParameters(jwt, "?idsOnly=false")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr...')  # só é válido para atributos estáticos
        res = self.getDevicesWithParameters(jwt, "?attr=serial=indefinido")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: label...')
        res = self.getDevicesWithParameters(jwt, "?label=test_device")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: sortBy...')
        res = self.getDevicesWithParameters(jwt, "?sortBy=label")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=integer...')
        res = self.getDevicesWithParameters(jwt, "?attr_type=integer")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=float...')
        res = self.getDevicesWithParameters(jwt, "?attr_type=float")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=string...')
        res = self.getDevicesWithParameters(jwt, "?attr_type=string")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=bool...')
        res = self.getDevicesWithParameters(jwt, "?attr_type=bool")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=geo:point...')
        res = self.getDevicesWithParameters(jwt, "?attr_type=geo:point")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameter: attr_type=object...')
        res = self.getDevicesWithParameters(jwt, "?attr_type=object")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with all parameters...')
        res = self.getDevicesWithParameters(jwt, "?page_size=2&page_num=1&idsOnly=true&attr_type=string&attr=serial=indefinido&label=dispositivo&sortBy=label")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameters (no match): return empty...')
        res = self.getDevicesWithParameters(jwt,
                                            "?page_size=2&page_num=1&idsOnly=false&attr_type=string&attr=serial=undefined&label=device&sortBy=label")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices with parameters (nonexistent parameter ): return full...')
        res = self.getDevicesWithParameters(jwt, "?parametro=outro")
        self.logger.debug('Devices: ' + str(res))

        self.logger.info('listing devices associated with given template...')
        res = self.getDevicesWithParameters(jwt, "/template/1")
        self.logger.debug('Result: ' + str(res))

        self.logger.info('listing devices associated with given template - page_num...')
        res = self.getDevicesWithParameters(jwt, "/template/1?page_num=1")
        self.logger.debug('Result: ' + str(res))

        self.logger.info('listing devices associated with given template - page_size...')
        res = self.getDevicesWithParameters(jwt, "/template/1?page_size=2")
        self.logger.debug('Result: ' + str(res))

        self.logger.info('listing devices associated with given template - page_num e page_size...')
        res = self.getDevicesWithParameters(jwt, "/template/1?page_size=2&page_num=2")
        self.logger.debug('Result: ' + str(res))




        """
        Lista device especifico
        """

        self.logger.info('listing specific device - device_id...')
        res = self.getDevice(jwt, Api.get_deviceid_by_label(jwt, 'sensor'))
        self.logger.debug('Device info: ' + str(res))

        self.logger.info('listing specific device - label...')
        res = self.getDevicesWithParameters(jwt, '?label=dispositivo')
        self.logger.debug('Device info: ' + str(res))

        """
        Remove device especifico
        """
        """

        self.logger.info('removing specific device - device_id...')
        res = self.deleteDevice(jwt, device_id)
        self.logger.info('Result: ' + str(res))

        self.logger.info('removing specific device - label...')
        res = self.deleteDevice(jwt, 'test_device_0')
        self.logger.info('Result: ' + str(res))
       """

        """
        Remove all devices
        """

        """
        self.logger.info('removing all devices...')
        res = self.deleteDevices(jwt)
        self.logger.debug('Result: ' + str(res))
        """

        """
        Fluxos Alternativos
        """

        """
        POST
        """

        self.logger.info('creating device - No such template...')

        devices = []
        devices.append(("1000", "teste"))
        result = self.createDevices(jwt, devices)
        self.logger.info("Result: " + str(result))


        self.logger.info('creating devices with count & verbose ...- Verbose can only be used for single device creation')
        result = self.createMultipleDevices(jwt, template_ids[1], 'test', "count=3&verbose=true")
        self.logger.info('Result: ' + str(result))

        self.logger.info('creating devices - count must be integer ...')
        result = self.createMultipleDevices(jwt, template_ids[1], 'test', "count=true")
        self.logger.info('Result: ' + str(result))

        #TODO: 'creating devices - Payload must be valid JSON...' (tem como provocar o erro?)

        #TODO: 'creating devices - Missing data for required field ...'

        #TODO:  'a device can not have repeated attributes' (device tem 2 atributos iguais de templates diferentes)

        #TODO: 'Failed to generate unique device_id' (é erro interno)

        """
        GET
        """

        self.logger.info('listing device - No such device...')
        res = self.getDevice(jwt, "123")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing device - internal error...')
        res = self.getDevicesWithParameters(jwt, "?page_num=")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing devices with parameter: Page numbers must be greater than 1...')
        res = self.getDevicesWithParameters(jwt, "?page_num=0")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing devices with parameter: At least one entry per page is mandatory...')
        res = self.getDevicesWithParameters(jwt, "?page_size=0")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing devices with parameter: page_size and page_num must be integers...')
        res = self.getDevicesWithParameters(jwt, "?page_num=xyz&page_size=kwv")
        self.logger.info('Result: ' + str(res))

        """
        GET - list of devices associated with given template
        GET/device/template/{template_id}{?page_size,page_num}
        """
        self.logger.info('listing devices associated with given template - At least one entry per page is mandatory...')
        res = self.getDevicesWithParameters(jwt, "/template/1?page_size=0")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing devices associated with given template - Page numbers must be greater than 1...')
        res = self.getDevicesWithParameters(jwt, "/template/1?page_num=0")
        self.logger.info('Result: ' + str(res))

        self.logger.info('listing devices associated with given template - page_size and page_num must be integers...')
        res = self.getDevicesWithParameters(jwt, "/template/1?page_num=kwv&page_size=xyz")
        self.logger.info('Result: ' + str(res))


        """
        PUT  /device/{id}
        """

        # TODO: 'updating device - Payload must be valid JSON, and Content-Type set accordingly'

        # TODO: 'updating device - Missing data for required field.'

        # TODO: 'updating device - a device can not have repeated attributes'

        # TODO: 'updating device - No such device: aaaa'

        # TODO: 'updating specific device - No such device...'

        # TODO: 'updating device - No such template: 4685'

        # TODO: 'updating device - Unknown template 4865 in attr list'

        # TODO: 'updating device - Unknown attribute 2 in override list'

        # TODO: 'updating device - Unknown metadata attribute 2 in override list'

        """
        Configure device - PUT /device/{id}/actuate
        """

        # TODO: 'updating device - No such device: aaaa'

        # TODO: 'updating device - some of the attributes are not configurable'

        """
        DELETE
        """

        self.logger.info('removing specific device - No such device...')
        res = self.deleteDevice(jwt, '123')
        self.logger.info('Result: ' + str(res))
