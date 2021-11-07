from __future__ import annotations
from typing import List, Tuple, Dict

try:
	import urequests as requests
except ImportError:
	import requests

try:
	import ujson as json
except ImportError:
	import json


class MethodTypeEnum():
	Get = 0
	Post = 1


class ApiInterface():

	def __init__(self, *, api_base_url: str):

		self.__api_base_url = api_base_url

	def _get_json_result_from_url(self, *, method_type, url: str, arguments_json_object: dict) -> dict:

		print("Trying to " + str(method_type) + " to \"" + url + "\"...")

		if method_type == MethodTypeEnum.Get:
			_response = requests.get(url, json=arguments_json_object)
		elif method_type == MethodTypeEnum.Post:
			_response = requests.post(url, json=arguments_json_object)
		else:
			raise NotImplementedError()

		if _response.status_code != 200:
			raise Exception("Unexpected status code: " + str(_response.status_code) + ": " + str(_response.reason) + ". Error: \"" + str(_response.text) + "\".")
		else:
			_json_response = _response.json()
			if "is_successful" not in _json_response:
				raise Exception("Unexpected missing key \"is_successful\": " + str(_json_response))
			elif "response" not in _json_response:
				raise Exception("Unexpected missing key \"response\": " + str(_json_response))
			elif "error" not in _json_response:
				raise Exception("Unexpected missing key \"error\": " + str(_json_response))
			else:
				_is_successful = _json_response["is_successful"]
				_response_value = _json_response["response"]
				_error = _json_response["error"]
				if not _is_successful:
					raise Exception("Error from messaging system: \"" + str(_error) + "\".")
				else:
					return _response_value

	def _get_formatted_url(self, *, url_part: str) -> str:
		return self.__api_base_url + url_part


class ComponentManagerApiInterface(ApiInterface):

	def __init__(self, component_manager_api_url: str):
		super().__init__(
			api_base_url=component_manager_api_url
		)

	def get_docker_api_specification(self) -> Dict:

		return self._get_json_result_from_url(
			method_type=MethodTypeEnum.Post,
			url=self._get_formatted_url(
				url_part="/v1/api/component_manager/get_docker_api_specification"
			),
			arguments_json_object={}
		)

	def get_docker_component_specification_by_component_uuid(self, *, component_uuid: str) -> Dict:

		return self._get_json_result_from_url(
			method_type=MethodTypeEnum.Post,
			url=self._get_formatted_url(
				url_part="/v1/api/component_manager/get_docker_component_specification_by_component_uuid"
			),
			arguments_json_object={
				"component_uuid": component_uuid
			}
		)
